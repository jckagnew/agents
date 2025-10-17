/**
 * Weight Tracker - Paywall Screen
 * Pro upgrade with Google Material illustration style
 * Hero illustration style like Google Material (flat, friendly)
 */

import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  Linking,
  Dimensions,
} from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { useWeightTrackerStore, useGatingFlags } from '../store';
import { Button, ScreenHeader } from '../components';
import { theme } from '../theme';

const { width: screenWidth } = Dimensions.get('window');

interface PaywallScreenProps {
  navigation: any;
}

export const PaywallScreen: React.FC<PaywallScreenProps> = ({ navigation }) => {
  const { updateSettings } = useWeightTrackerStore();
  const gatingFlags = useGatingFlags();
  const [isLoading, setIsLoading] = useState(false);

  const handlePurchase = async (plan: 'monthly' | 'yearly') => {
    setIsLoading(true);
    
    try {
      // Simulate purchase process
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Update user to pro
      updateSettings({
        plan: 'pro',
        // Add other pro settings here
      });
      
      Alert.alert(
        'Welcome to Pro!',
        'You now have access to all premium features.',
        [
          {
            text: 'Get Started',
            onPress: () => navigation.goBack(),
          },
        ]
      );
    } catch (error) {
      Alert.alert('Error', 'Failed to process purchase. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleRestore = () => {
    Alert.alert(
      'Restore Purchases',
      'This will restore your previous purchases if you have any.',
      [
        { text: 'Cancel', style: 'cancel' },
        {
          text: 'Restore',
          onPress: async () => {
            setIsLoading(true);
            try {
              // Simulate restore process
              await new Promise(resolve => setTimeout(resolve, 1500));
              Alert.alert('Success', 'Purchases restored successfully!');
            } catch (error) {
              Alert.alert('Error', 'No purchases found to restore.');
            } finally {
              setIsLoading(false);
            }
          },
        },
      ]
    );
  };

  const handleTerms = () => {
    Linking.openURL('https://example.com/terms-of-service');
  };

  const handlePrivacy = () => {
    Linking.openURL('https://example.com/privacy-policy');
  };

  const features = [
    {
      icon: 'trending-up',
      title: 'Advanced Analytics',
      description: 'Detailed insights and trend analysis',
    },
    {
      icon: 'smooth',
      title: 'Custom Smoothing',
      description: 'Adjustable data smoothing controls',
    },
    {
      icon: 'analytics',
      title: 'WHR Trends',
      description: 'Waist-to-hip ratio trend tracking',
    },
    {
      icon: 'target',
      title: 'Moving Goals',
      description: 'Dynamic goal adjustment based on progress',
    },
    {
      icon: 'infinite',
      title: 'Unlimited Entries',
      description: 'Log multiple entries per day',
    },
    {
      icon: 'cloud',
      title: 'Cloud Sync',
      description: 'Sync data across all your devices',
    },
  ];

  const getFeatureTintColor = (index: number): string => {
    const colors = [theme.colors.tintBlue, theme.colors.tintGreen, theme.colors.tintYellow];
    return colors[index % colors.length];
  };

  const getFeatureIconColor = (index: number): string => {
    const colors = [theme.colors.primary, theme.colors.success, theme.colors.secondary];
    return colors[index % colors.length];
  };

  return (
    <ScrollView style={styles.container}>
      <ScreenHeader
        title="Upgrade to Pro"
        subtitle="Unlock advanced features and insights"
        leftIcon="arrow-back"
        onPressLeft={() => navigation.goBack()}
        leftIconAccessibilityLabel="Back to previous screen"
        containerStyle={styles.header}
      />

      {/* Hero Illustration Section - Google Material Style */}
      <View style={styles.heroSection}>
        <View style={styles.illustrationContainer}>
          {/* Google Material Style Characters */}
          <View style={styles.characterContainer}>
            <View style={[styles.character, styles.character1]}>
              <Ionicons name="trending-up" size={32} color={theme.colors.primary} />
            </View>
            <View style={[styles.character, styles.character2]}>
              <Ionicons name="analytics" size={28} color={theme.colors.success} />
            </View>
            <View style={[styles.character, styles.character3]}>
              <Ionicons name="diamond" size={24} color={theme.colors.secondary} />
            </View>
          </View>
          
          {/* Floating Elements */}
          <View style={styles.floatingElements}>
            <View style={[styles.floatingElement, styles.floating1]}>
              <Ionicons name="checkmark-circle" size={16} color={theme.colors.success} />
            </View>
            <View style={[styles.floatingElement, styles.floating2]}>
              <Ionicons name="star" size={14} color={theme.colors.secondary} />
            </View>
            <View style={[styles.floatingElement, styles.floating3]}>
              <Ionicons name="heart" size={12} color={theme.colors.error} />
            </View>
          </View>
        </View>
        
        <Text style={styles.heroTitle}>Take Your Tracking to the Next Level</Text>
        <Text style={styles.heroSubtitle}>
          Get detailed insights, advanced analytics, and personalized recommendations
        </Text>
      </View>

      {/* Features Grid - Card Layout */}
      <View style={styles.featuresSection}>
        <Text style={styles.featuresTitle}>Pro Features</Text>
        <View style={styles.featuresGrid}>
          {features.map((feature, index) => (
            <View key={index} style={styles.featureCard}>
              <View style={[styles.featureIcon, { backgroundColor: getFeatureTintColor(index) }]}>
                <Ionicons name={feature.icon as any} size={24} color={getFeatureIconColor(index)} />
              </View>
              <Text style={styles.featureTitle}>{feature.title}</Text>
              <Text style={styles.featureDescription}>{feature.description}</Text>
            </View>
          ))}
        </View>
      </View>

      {/* Pricing Cards - Free vs Pro Tiers */}
      <View style={styles.pricingSection}>
        <Text style={styles.pricingTitle}>Choose Your Plan</Text>
        
        {/* Free Tier */}
        <View style={[styles.pricingCard, styles.freeTier]}>
          <View style={styles.tierHeader}>
            <Text style={styles.tierTitle}>Free</Text>
            <Text style={styles.tierPrice}>$0/month</Text>
          </View>
          <View style={styles.tierFeatures}>
            <View style={styles.tierFeature}>
              <Ionicons name="checkmark" size={16} color={theme.colors.success} />
              <Text style={styles.tierFeatureText}>Basic weight tracking</Text>
            </View>
            <View style={styles.tierFeature}>
              <Ionicons name="checkmark" size={16} color={theme.colors.success} />
              <Text style={styles.tierFeatureText}>One entry per day</Text>
            </View>
            <View style={styles.tierFeature}>
              <Ionicons name="checkmark" size={16} color={theme.colors.success} />
              <Text style={styles.tierFeatureText}>Basic charts</Text>
            </View>
          </View>
        </View>

        {/* Pro Tier */}
        <TouchableOpacity
          style={[styles.pricingCard, styles.proTier]}
          onPress={() => handlePurchase('yearly')}
          disabled={isLoading}
        >
          <View style={styles.recommendedBadge}>
            <Text style={styles.recommendedText}>RECOMMENDED</Text>
          </View>
          <View style={styles.tierHeader}>
            <Text style={styles.tierTitle}>Pro</Text>
            <Text style={styles.tierPrice}>$29.99/year</Text>
            <Text style={styles.tierSavings}>Save 50% vs monthly</Text>
          </View>
          <View style={styles.tierFeatures}>
            <View style={styles.tierFeature}>
              <Ionicons name="checkmark" size={16} color={theme.colors.success} />
              <Text style={styles.tierFeatureText}>Everything in Free</Text>
            </View>
            <View style={styles.tierFeature}>
              <Ionicons name="checkmark" size={16} color={theme.colors.success} />
              <Text style={styles.tierFeatureText}>Advanced analytics</Text>
            </View>
            <View style={styles.tierFeature}>
              <Ionicons name="checkmark" size={16} color={theme.colors.success} />
              <Text style={styles.tierFeatureText}>Unlimited entries</Text>
            </View>
            <View style={styles.tierFeature}>
              <Ionicons name="checkmark" size={16} color={theme.colors.success} />
              <Text style={styles.tierFeatureText}>Cloud sync</Text>
            </View>
            <View style={styles.tierFeature}>
              <Ionicons name="checkmark" size={16} color={theme.colors.success} />
              <Text style={styles.tierFeatureText}>Custom smoothing</Text>
            </View>
          </View>
        </TouchableOpacity>
      </View>

      {/* Benefits Section */}
      <View style={styles.benefitsSection}>
        <Text style={styles.benefitsTitle}>Why Go Pro?</Text>
        
        <View style={styles.benefitsGrid}>
          <View style={styles.benefitCard}>
            <Ionicons name="shield-checkmark" size={24} color={theme.colors.success} />
            <Text style={styles.benefitTitle}>Privacy-First</Text>
            <Text style={styles.benefitText}>Your data stays on your device</Text>
          </View>
          
          <View style={styles.benefitCard}>
            <Ionicons name="rocket" size={24} color={theme.colors.primary} />
            <Text style={styles.benefitTitle}>Advanced AI</Text>
            <Text style={styles.benefitText}>Better insights with smart algorithms</Text>
          </View>
          
          <View style={styles.benefitCard}>
            <Ionicons name="trending-up" size={24} color={theme.colors.secondary} />
            <Text style={styles.benefitTitle}>Detailed Analytics</Text>
            <Text style={styles.benefitText}>Track progress with precision</Text>
          </View>
          
          <View style={styles.benefitCard}>
            <Ionicons name="sync" size={24} color={theme.colors.info} />
            <Text style={styles.benefitTitle}>Cloud Sync</Text>
            <Text style={styles.benefitText}>Access from all your devices</Text>
          </View>
        </View>
      </View>

      {/* Footer */}
      <View style={styles.footer}>
        <Button
          title="Restore Purchases"
          onPress={handleRestore}
          variant="outline"
          disabled={isLoading}
          style={styles.restoreButton}
        />
        
        <View style={styles.legalLinks}>
          <TouchableOpacity onPress={handleTerms}>
            <Text style={styles.legalLink}>Terms of Service</Text>
          </TouchableOpacity>
          <Text style={styles.legalSeparator}>•</Text>
          <TouchableOpacity onPress={handlePrivacy}>
            <Text style={styles.legalLink}>Privacy Policy</Text>
          </TouchableOpacity>
        </View>
        
        <Text style={styles.disclaimer}>
          Subscriptions automatically renew unless auto-renew is turned off at least 24 hours before the end of the current period.
        </Text>
      </View>

      {/* Loading Overlay */}
      {isLoading && (
        <View style={styles.loadingOverlay}>
          <View style={styles.loadingContainer}>
            <Text style={styles.loadingText}>Processing...</Text>
          </View>
        </View>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: theme.colors.background,
  },
  header: {
    borderBottomLeftRadius: 0,
    borderBottomRightRadius: 0,
  },
  // Hero Section with Google Material Illustration
  heroSection: {
    alignItems: 'center',
    padding: theme.spacing['4xl'],
    backgroundColor: theme.colors.surface,
  },
  illustrationContainer: {
    position: 'relative',
    width: screenWidth * 0.8,
    height: 200,
    marginBottom: theme.spacing.xl,
  },
  characterContainer: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    justifyContent: 'center',
    alignItems: 'center',
  },
  character: {
    position: 'absolute',
    width: 60,
    height: 60,
    borderRadius: 30,
    justifyContent: 'center',
    alignItems: 'center',
    ...theme.shadows.md,
  },
  character1: {
    backgroundColor: theme.colors.tintBlue,
    top: 20,
    left: 20,
  },
  character2: {
    backgroundColor: theme.colors.tintGreen,
    top: 40,
    right: 30,
  },
  character3: {
    backgroundColor: theme.colors.tintYellow,
    bottom: 30,
    left: '50%',
    marginLeft: -30,
  },
  floatingElements: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
  },
  floatingElement: {
    position: 'absolute',
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: theme.colors.surface,
    justifyContent: 'center',
    alignItems: 'center',
    ...theme.shadows.sm,
  },
  floating1: {
    top: 60,
    right: 60,
  },
  floating2: {
    top: 100,
    left: 40,
  },
  floating3: {
    bottom: 60,
    right: 40,
  },
  heroTitle: {
    fontSize: theme.typography.fontSize.h1,
    fontFamily: theme.typography.fontFamily.heading,
    color: theme.colors.textPrimary,
    textAlign: 'center',
    marginBottom: theme.spacing.md,
    letterSpacing: theme.typography.letterSpacing.tight,
  },
  heroSubtitle: {
    fontSize: theme.typography.fontSize.bodyLg,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textSecondary,
    textAlign: 'center',
    lineHeight: theme.typography.lineHeight.relaxed * theme.typography.fontSize.bodyLg,
  },
  // Features Section
  featuresSection: {
    margin: theme.spacing.lg,
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.xl,
    padding: theme.spacing.lg,
    ...theme.shadows.md,
  },
  featuresTitle: {
    fontSize: theme.typography.fontSize.h2,
    fontFamily: theme.typography.fontFamily.heading,
    color: theme.colors.textPrimary,
    marginBottom: theme.spacing.lg,
    textAlign: 'center',
  },
  featuresGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: theme.spacing.md,
  },
  featureCard: {
    width: (screenWidth - theme.spacing.lg * 2 - theme.spacing.md) / 2,
    backgroundColor: theme.colors.background,
    borderRadius: theme.borderRadius.lg,
    padding: theme.spacing.md,
    alignItems: 'center',
    ...theme.shadows.sm,
  },
  featureIcon: {
    width: 48,
    height: 48,
    borderRadius: 24,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: theme.spacing.sm,
  },
  featureTitle: {
    fontSize: theme.typography.fontSize.label,
    fontFamily: theme.typography.fontFamily.label,
    color: theme.colors.textPrimary,
    marginBottom: theme.spacing.xs,
    textAlign: 'center',
  },
  featureDescription: {
    fontSize: theme.typography.fontSize.small,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textSecondary,
    textAlign: 'center',
  },
  // Pricing Section
  pricingSection: {
    margin: theme.spacing.lg,
    gap: theme.spacing.md,
  },
  pricingTitle: {
    fontSize: theme.typography.fontSize.h2,
    fontFamily: theme.typography.fontFamily.heading,
    color: theme.colors.textPrimary,
    textAlign: 'center',
    marginBottom: theme.spacing.lg,
  },
  pricingCard: {
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.xl,
    padding: theme.spacing.lg,
    ...theme.shadows.md,
    position: 'relative',
  },
  freeTier: {
    borderWidth: 1,
    borderColor: theme.colors.border,
  },
  proTier: {
    borderWidth: 2,
    borderColor: theme.colors.primary,
  },
  recommendedBadge: {
    position: 'absolute',
    top: -8,
    left: '50%',
    marginLeft: -50,
    backgroundColor: theme.colors.primary,
    paddingHorizontal: theme.spacing.md,
    paddingVertical: theme.spacing.xs,
    borderRadius: theme.borderRadius.full,
  },
  recommendedText: {
    color: theme.colors.textInverse,
    fontSize: theme.typography.fontSize.small,
    fontFamily: theme.typography.fontFamily.label,
  },
  tierHeader: {
    alignItems: 'center',
    marginBottom: theme.spacing.lg,
  },
  tierTitle: {
    fontSize: theme.typography.fontSize.h3,
    fontFamily: theme.typography.fontFamily.heading,
    color: theme.colors.textPrimary,
    marginBottom: theme.spacing.sm,
  },
  tierPrice: {
    fontSize: theme.typography.fontSize.h1,
    fontFamily: theme.typography.fontFamily.heading,
    color: theme.colors.primary,
    marginBottom: theme.spacing.xs,
  },
  tierSavings: {
    fontSize: theme.typography.fontSize.label,
    fontFamily: theme.typography.fontFamily.label,
    color: theme.colors.success,
  },
  tierFeatures: {
    gap: theme.spacing.sm,
  },
  tierFeature: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  tierFeatureText: {
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textPrimary,
    marginLeft: theme.spacing.sm,
  },
  // Benefits Section
  benefitsSection: {
    margin: theme.spacing.lg,
    backgroundColor: theme.colors.surface,
    borderRadius: theme.borderRadius.xl,
    padding: theme.spacing.lg,
    ...theme.shadows.md,
  },
  benefitsTitle: {
    fontSize: theme.typography.fontSize.h2,
    fontFamily: theme.typography.fontFamily.heading,
    color: theme.colors.textPrimary,
    marginBottom: theme.spacing.lg,
    textAlign: 'center',
  },
  benefitsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: theme.spacing.md,
  },
  benefitCard: {
    width: (screenWidth - theme.spacing.lg * 2 - theme.spacing.md) / 2,
    backgroundColor: theme.colors.background,
    borderRadius: theme.borderRadius.lg,
    padding: theme.spacing.md,
    alignItems: 'center',
    ...theme.shadows.sm,
  },
  benefitTitle: {
    fontSize: theme.typography.fontSize.label,
    fontFamily: theme.typography.fontFamily.label,
    color: theme.colors.textPrimary,
    marginTop: theme.spacing.sm,
    marginBottom: theme.spacing.xs,
    textAlign: 'center',
  },
  benefitText: {
    fontSize: theme.typography.fontSize.small,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textSecondary,
    textAlign: 'center',
  },
  // Footer
  footer: {
    padding: theme.spacing.lg,
    alignItems: 'center',
  },
  restoreButton: {
    marginBottom: theme.spacing.lg,
  },
  legalLinks: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: theme.spacing.md,
  },
  legalLink: {
    fontSize: theme.typography.fontSize.label,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.primary,
  },
  legalSeparator: {
    fontSize: theme.typography.fontSize.label,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textSecondary,
    marginHorizontal: theme.spacing.sm,
  },
  disclaimer: {
    fontSize: theme.typography.fontSize.small,
    fontFamily: theme.typography.fontFamily.body,
    color: theme.colors.textSecondary,
    textAlign: 'center',
    lineHeight: theme.typography.lineHeight.relaxed * theme.typography.fontSize.small,
  },
  // Loading Overlay
  loadingOverlay: {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingContainer: {
    backgroundColor: theme.colors.surface,
    padding: theme.spacing.lg,
    borderRadius: theme.borderRadius.lg,
    alignItems: 'center',
    ...theme.shadows.lg,
  },
  loadingText: {
    fontSize: theme.typography.fontSize.body,
    fontFamily: theme.typography.fontFamily.label,
    color: theme.colors.textPrimary,
  },
});
