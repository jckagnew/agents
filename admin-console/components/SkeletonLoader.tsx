import { View, StyleSheet, Animated, useEffect, useRef } from 'react-native';

export function SkeletonLoader({ width = '100%', height = 20, borderRadius = 4 }) {
  const shimmerAnimation = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(shimmerAnimation, {
          toValue: 1,
          duration: 1000,
          useNativeDriver: true,
        }),
        Animated.timing(shimmerAnimation, {
          toValue: 0,
          duration: 1000,
          useNativeDriver: true,
        }),
      ])
    ).start();
  }, []);

  const opacity = shimmerAnimation.interpolate({
    inputRange: [0, 1],
    outputRange: [0.3, 0.7],
  });

  return (
    <Animated.View
      style={[
        styles.skeleton,
        {
          width,
          height,
          borderRadius,
          opacity,
        },
      ]}
    />
  );
}

export function CustomerCardSkeleton() {
  return (
    <View style={styles.card}>
      <View style={styles.cardHeader}>
        <View style={{ flex: 1 }}>
          <SkeletonLoader width="60%" height={20} borderRadius={4} />
          <View style={{ height: 8 }} />
          <SkeletonLoader width="40%" height={14} borderRadius={4} />
        </View>
        <SkeletonLoader width={60} height={24} borderRadius={6} />
      </View>
      <View style={{ height: 8 }} />
      <SkeletonLoader width="80%" height={14} borderRadius={4} />
      <View style={{ height: 12 }} />
      <View style={styles.footer}>
        <SkeletonLoader width={80} height={12} borderRadius={4} />
        <SkeletonLoader width={60} height={12} borderRadius={4} />
        <SkeletonLoader width={70} height={12} borderRadius={4} />
      </View>
    </View>
  );
}

export function ProjectCardSkeleton() {
  return (
    <View style={styles.card}>
      <View style={styles.cardHeader}>
        <View style={{ flex: 1, flexDirection: 'row', gap: 12 }}>
          <SkeletonLoader width={16} height={16} borderRadius={4} />
          <View style={{ flex: 1 }}>
            <SkeletonLoader width="70%" height={20} borderRadius={4} />
            <View style={{ height: 6 }} />
            <SkeletonLoader width="50%" height={14} borderRadius={4} />
          </View>
        </View>
        <SkeletonLoader width={60} height={24} borderRadius={6} />
      </View>
      <View style={{ height: 12 }} />
      <SkeletonLoader width="90%" height={14} borderRadius={4} />
      <View style={{ height: 4 }} />
      <SkeletonLoader width="70%" height={14} borderRadius={4} />
      <View style={{ height: 12 }} />
      <View style={styles.footer}>
        <SkeletonLoader width={100} height={12} borderRadius={4} />
        <SkeletonLoader width={80} height={12} borderRadius={4} />
      </View>
    </View>
  );
}

export function ListSkeleton({ count = 5, type = 'customer' }) {
  const SkeletonCard = type === 'customer' ? CustomerCardSkeleton : ProjectCardSkeleton;

  return (
    <View style={styles.container}>
      {Array.from({ length: count }).map((_, index) => (
        <SkeletonCard key={index} />
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  skeleton: {
    backgroundColor: '#E5E5EA',
  },
  container: {
    paddingHorizontal: 16,
    paddingTop: 16,
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: 12,
    padding: 16,
    marginBottom: 12,
    borderWidth: 1,
    borderColor: '#E5E5EA',
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
  },
  footer: {
    flexDirection: 'row',
    gap: 16,
  },
});
