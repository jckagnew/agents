/**
 * Input validation schemas using Zod
 * Prevents injection attacks, XSS, and bad data
 */
import { z } from 'https://deno.land/x/zod@v3.22.4/mod.ts';

// Email validation
export const emailSchema = z.string().email().max(255);

// Phone validation (international format)
export const phoneSchema = z.string().regex(/^\+?[1-9]\d{1,14}$/).optional().or(z.literal(''));

// UUID validation
export const uuidSchema = z.string().uuid();

// Safe text fields (prevent XSS)
export const safeTextSchema = (maxLength = 500) =>
  z.string()
    .max(maxLength)
    .transform(str => str.trim())
    .refine(
      str => !/<script|javascript:|on\w+=/i.test(str),
      'Invalid characters detected'
    );

// Customer validation schemas
export const createCustomerSchema = z.object({
  full_name: safeTextSchema(255),
  email: emailSchema,
  phone: phoneSchema,
  company_name: safeTextSchema(255).optional(),
  subscription_status: z.enum(['none', 'trial', 'active', 'cancelled', 'past_due']).default('none'),
  subscription_tier: z.enum(['free', 'basic', 'pro', 'enterprise']).optional(),
  source: safeTextSchema(100).optional(),
  tags: z.array(safeTextSchema(50)).max(10).default([]),
});

export const updateCustomerSchema = z.object({
  full_name: safeTextSchema(255).optional(),
  email: emailSchema.optional(),
  phone: phoneSchema,
  company_name: safeTextSchema(255).optional(),
  subscription_status: z.enum(['none', 'trial', 'active', 'cancelled', 'past_due']).optional(),
  subscription_tier: z.enum(['free', 'basic', 'pro', 'enterprise']).optional(),
  status: z.enum(['active', 'inactive']).optional(),
  tags: z.array(safeTextSchema(50)).max(10).optional(),
  notes: safeTextSchema(2000).optional(),
});

// Project validation schemas
export const createProjectSchema = z.object({
  customer_id: uuidSchema,
  name: safeTextSchema(255),
  description: safeTextSchema(2000).optional(),
  status: z.enum(['planning', 'active', 'on-hold', 'completed', 'cancelled']).default('planning'),
  start_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
  end_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
  budget: z.number().min(0).max(10000000).optional(),
  tags: z.array(safeTextSchema(50)).max(10).default([]),
}).refine(
  data => !data.start_date || !data.end_date || data.end_date >= data.start_date,
  {
    message: 'End date must be after start date',
    path: ['end_date'],
  }
);

export const updateProjectSchema = z.object({
  name: safeTextSchema(255).optional(),
  description: safeTextSchema(2000).optional(),
  status: z.enum(['planning', 'active', 'on-hold', 'completed', 'cancelled']).optional(),
  start_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
  end_date: z.string().regex(/^\d{4}-\d{2}-\d{2}$/).optional(),
  budget: z.number().min(0).max(10000000).optional(),
  tags: z.array(safeTextSchema(50)).max(10).optional(),
}).refine(
  data => !data.start_date || !data.end_date || data.end_date >= data.start_date,
  {
    message: 'End date must be after start date',
    path: ['end_date'],
  }
);

// Pagination validation
export const paginationSchema = z.object({
  page: z.number().int().min(1).default(1),
  limit: z.number().int().min(1).max(100).default(20),
});

// Search validation
export const searchSchema = safeTextSchema(100).optional();

/**
 * Validate and sanitize input data
 */
export function validateInput<T>(schema: z.ZodSchema<T>, data: unknown): {
  success: boolean;
  data?: T;
  errors?: string[];
} {
  try {
    const result = schema.parse(data);
    return { success: true, data: result };
  } catch (error) {
    if (error instanceof z.ZodError) {
      return {
        success: false,
        errors: error.errors.map(err => `${err.path.join('.')}: ${err.message}`),
      };
    }
    return { success: false, errors: ['Validation failed'] };
  }
}
