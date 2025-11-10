import { serve } from 'https://deno.land/std@0.168.0/http/server.ts';
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
import Stripe from 'https://esm.sh/stripe@14.21.0';

const stripe = new Stripe(Deno.env.get('STRIPE_SECRET_KEY')!, {
  apiVersion: '2023-10-16',
});

serve(async (req) => {
  const signature = req.headers.get('stripe-signature');
  const webhookSecret = Deno.env.get('STRIPE_WEBHOOK_SECRET');

  if (!signature || !webhookSecret) {
    return new Response(JSON.stringify({ error: 'Missing signature or webhook secret' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }

  try {
    const body = await req.text();
    const event = stripe.webhooks.constructEvent(body, signature, webhookSecret);

    // Use service role client for database operations
    const supabase = createClient(
      Deno.env.get('SUPABASE_URL')!,
      Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
    );

    switch (event.type) {
      case 'customer.created': {
        const customer = event.data.object as Stripe.Customer;

        // Link Stripe customer to our customer record if email matches
        if (customer.email) {
          await supabase
            .from('customers')
            .update({ stripe_customer_id: customer.id })
            .eq('email', customer.email);
        }
        break;
      }

      case 'customer.subscription.created':
      case 'customer.subscription.updated': {
        const subscription = event.data.object as Stripe.Subscription;

        await supabase
          .from('customers')
          .update({
            subscription_status: subscription.status === 'active' ? 'active' : subscription.status,
            mrr: subscription.items.data[0]?.price?.unit_amount
              ? subscription.items.data[0].price.unit_amount / 100
              : 0,
          })
          .eq('stripe_customer_id', subscription.customer as string);
        break;
      }

      case 'customer.subscription.deleted': {
        const subscription = event.data.object as Stripe.Subscription;

        await supabase
          .from('customers')
          .update({
            subscription_status: 'cancelled',
            mrr: 0,
          })
          .eq('stripe_customer_id', subscription.customer as string);
        break;
      }

      case 'invoice.created': {
        const invoice = event.data.object as Stripe.Invoice;

        // Get customer from our database
        const { data: customer } = await supabase
          .from('customers')
          .select('id')
          .eq('stripe_customer_id', invoice.customer as string)
          .single();

        if (customer) {
          await supabase.from('invoices').insert({
            customer_id: customer.id,
            stripe_invoice_id: invoice.id,
            amount: invoice.amount_due / 100,
            currency: invoice.currency.toUpperCase(),
            status: 'sent',
            due_date: invoice.due_date ? new Date(invoice.due_date * 1000).toISOString() : null,
            line_items: invoice.lines.data.map((line) => ({
              description: line.description,
              amount: line.amount / 100,
            })),
          });
        }
        break;
      }

      case 'invoice.paid': {
        const invoice = event.data.object as Stripe.Invoice;

        await supabase
          .from('invoices')
          .update({
            status: 'paid',
            paid_at: new Date(invoice.status_transitions.paid_at! * 1000).toISOString(),
          })
          .eq('stripe_invoice_id', invoice.id);
        break;
      }

      case 'invoice.payment_failed': {
        const invoice = event.data.object as Stripe.Invoice;

        await supabase
          .from('invoices')
          .update({ status: 'failed' })
          .eq('stripe_invoice_id', invoice.id);

        // Update customer status to past_due
        const { data: invoiceRecord } = await supabase
          .from('invoices')
          .select('customer_id')
          .eq('stripe_invoice_id', invoice.id)
          .single();

        if (invoiceRecord) {
          await supabase
            .from('customers')
            .update({ subscription_status: 'past_due' })
            .eq('id', invoiceRecord.customer_id);
        }
        break;
      }

      case 'charge.refunded': {
        const charge = event.data.object as Stripe.Charge;

        if (charge.invoice) {
          await supabase
            .from('invoices')
            .update({ status: 'refunded' })
            .eq('stripe_invoice_id', charge.invoice as string);
        }
        break;
      }

      default:
        console.log(`Unhandled event type: ${event.type}`);
    }

    return new Response(JSON.stringify({ received: true }), {
      status: 200,
      headers: { 'Content-Type': 'application/json' },
    });
  } catch (error) {
    console.error('Webhook error:', error.message);
    return new Response(JSON.stringify({ error: error.message }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    });
  }
});
