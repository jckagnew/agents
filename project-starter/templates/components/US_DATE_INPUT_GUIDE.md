# 📅 US Date Input Components - Project Starter

## Overview

This template provides smooth, non-jumpy date input components with US standard formatting (MM/DD/YYYY) for both mobile (React Native) and web (Next.js) projects.

## 🎯 Features

- **US Standard Format**: MM/DD/YYYY date format
- **Smooth Input**: Non-jumpy animations and transitions
- **Auto-formatting**: Automatically formats as user types
- **Validation**: Built-in date validation
- **Cross-platform**: Works on mobile and web
- **Accessibility**: Proper focus states and error handling

## 📱 Mobile Components (React Native)

### SmoothDateInput Component

```tsx
import SmoothDateInput from './components/SmoothDateInput';

<SmoothDateInput
  value={date}
  onChangeText={setDate}
  placeholder="MM/DD/YYYY"
  error={errors.date}
  onFocus={() => setFocusedField('date')}
  onBlur={() => setFocusedField(null)}
/>
```

### DateUtilityService

```tsx
import { dateUtilityService } from './services/DateUtilityService';

// Convert ISO to US format
const usDate = dateUtilityService.formatToUSDate('2024-01-15'); // "01/15/2024"

// Convert US to ISO format
const isoDate = dateUtilityService.parseFromUSDate('01/15/2024'); // "2024-01-15"

// Get today's date
const todayUS = dateUtilityService.getTodayUS(); // "01/15/2024"
const todayISO = dateUtilityService.getTodayISO(); // "2024-01-15"

// Format with day of week
const formatted = dateUtilityService.formatWithDayOfWeek('2024-01-15'); // "Monday, 01/15/2024"

// Validate date
const isValid = dateUtilityService.isValidUSDate('01/15/2024'); // true
```

## 🌐 Web Components (Next.js)

### SmoothDateInput Component

```tsx
import SmoothDateInput from '@/components/SmoothDateInput';

<SmoothDateInput
  value={date}
  onChangeText={setDate}
  placeholder="MM/DD/YYYY"
  error={errors.date}
  className="w-full"
/>
```

### DateUtilityService

```tsx
import { dateUtilityService } from '@/services/DateUtilityService';

// Same API as mobile version
const usDate = dateUtilityService.formatToUSDate('2024-01-15');
const isoDate = dateUtilityService.parseFromUSDate('01/15/2024');
```

## 🎨 Styling

### Mobile (React Native)
- Uses `StyleSheet` with modern design principles
- Smooth animations with `Animated` API
- Focus states with border color changes
- Error states with red borders

### Web (Next.js)
- Uses Tailwind CSS classes
- Smooth transitions with CSS
- Focus states with shadow effects
- Error states with red styling

## 📋 Usage Examples

### Form Integration

```tsx
// Mobile
const [formData, setFormData] = useState({
  date: dateUtilityService.getTodayUS(),
  // other fields...
});

const validateForm = () => {
  const errors = {};
  if (!dateUtilityService.isValidUSDate(formData.date)) {
    errors.date = 'Please enter a valid date (MM/DD/YYYY)';
  }
  return errors;
};

// Web
const [date, setDate] = useState(dateUtilityService.getTodayUS());
const [errors, setErrors] = useState({});

const handleSubmit = () => {
  const isoDate = dateUtilityService.parseFromUSDate(date);
  // Submit with ISO format for backend
};
```

### Display Formatting

```tsx
// Show relative dates
const displayDate = dateUtilityService.getRelativeDateDescription(record.date);
// "Today", "Yesterday", or "01/15/2024"

// Show with day of week
const fullDate = dateUtilityService.formatWithDayOfWeek(record.date);
// "Monday, 01/15/2024"
```

## 🔧 Customization

### Mobile Customization

```tsx
// Custom styles
const customStyles = StyleSheet.create({
  inputContainer: {
    backgroundColor: '#f8f9fa',
    borderColor: '#007bff',
    borderRadius: 8,
  },
});

<SmoothDateInput
  style={customStyles.inputContainer}
  // other props...
/>
```

### Web Customization

```tsx
// Custom Tailwind classes
<SmoothDateInput
  className="w-full px-6 py-4 text-lg border-2 border-blue-500 rounded-lg"
  // other props...
/>
```

## 🧪 Testing

### Validation Tests

```tsx
// Test date validation
expect(dateUtilityService.isValidUSDate('01/15/2024')).toBe(true);
expect(dateUtilityService.isValidUSDate('13/45/2024')).toBe(false);

// Test format conversion
expect(dateUtilityService.formatToUSDate('2024-01-15')).toBe('01/15/2024');
expect(dateUtilityService.parseFromUSDate('01/15/2024')).toBe('2024-01-15');
```

### Component Tests

```tsx
// Test auto-formatting
fireEvent.changeText(input, '01152024');
expect(input.props.value).toBe('01/15/2024');

// Test error states
expect(screen.getByText('Please enter a valid date')).toBeInTheDocument();
```

## 📚 API Reference

### SmoothDateInput Props

| Prop | Type | Default | Description |
|------|------|---------|-------------|
| `value` | `string` | - | Current date value in US format |
| `onChangeText` | `(value: string) => void` | - | Callback when value changes |
| `placeholder` | `string` | `'MM/DD/YYYY'` | Placeholder text |
| `error` | `string` | - | Error message to display |
| `onFocus` | `() => void` | - | Focus callback |
| `onBlur` | `() => void` | - | Blur callback |
| `style`/`className` | `any`/`string` | - | Custom styling |

### DateUtilityService Methods

| Method | Parameters | Returns | Description |
|--------|------------|---------|-------------|
| `formatToUSDate` | `isoDate: string` | `string` | Convert ISO to US format |
| `parseFromUSDate` | `usDate: string` | `string` | Convert US to ISO format |
| `getTodayUS` | - | `string` | Get today in US format |
| `getTodayISO` | - | `string` | Get today in ISO format |
| `formatWithDayOfWeek` | `isoDate: string` | `string` | Format with day name |
| `isValidUSDate` | `usDate: string` | `boolean` | Validate US date format |
| `getRelativeDateDescription` | `isoDate: string` | `string` | Get relative date |

## 🚀 Getting Started

1. **Copy Components**: Copy the component files to your project
2. **Import Services**: Import the DateUtilityService
3. **Add to Forms**: Use SmoothDateInput in your forms
4. **Validate Data**: Use the utility methods for validation
5. **Style as Needed**: Customize the appearance for your design

## 📝 Best Practices

- Always validate dates before submission
- Store dates in ISO format in your database
- Display dates in US format for users
- Use relative dates for recent entries
- Provide clear error messages for invalid dates
- Test with edge cases (leap years, invalid dates)

## 🔄 Migration Guide

If you're migrating from other date formats:

1. **Replace Date Pickers**: Replace existing date pickers with SmoothDateInput
2. **Update Validation**: Use DateUtilityService for validation
3. **Convert Existing Data**: Use formatToUSDate for display
4. **Update Forms**: Change form handling to use US format
5. **Test Thoroughly**: Ensure all date functionality works correctly

---

**Ready to use smooth, US-standard date inputs in your projects!** 🎉
