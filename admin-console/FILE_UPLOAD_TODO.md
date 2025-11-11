# File Upload Implementation

## Status: Pending

File upload for design files requires additional native modules and configuration that goes beyond basic Expo functionality.

## Requirements

1. **Expo Image Picker**
   ```bash
   npx expo install expo-image-picker expo-document-picker
   ```

2. **Permissions Configuration**
   - iOS: `NSPhotoLibraryUsageDescription`, `NSCameraUsageDescription`
   - Android: `READ_EXTERNAL_STORAGE`, `WRITE_EXTERNAL_STORAGE`, `CAMERA`

3. **Implementation Approach**

   Option A: **Expo Image Picker** (for images/photos)
   - Good for design mockups, screenshots
   - Built-in cropping and resizing
   - Works with camera or photo library

   Option B: **Expo Document Picker** (for files)
   - Good for Figma files, PDFs, etc.
   - Supports multiple file types
   - No preview functionality

4. **Code Skeleton**

```typescript
// hooks/useFileUpload.ts
import * as ImagePicker from 'expo-image-picker';
import * as DocumentPicker from 'expo-document-picker';
import { supabase } from '@/lib/supabase';

export function useFileUpload() {
  const pickImage = async () => {
    const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();
    if (status !== 'granted') {
      Alert.alert('Permission required', 'Please grant photo library access');
      return null;
    }

    const result = await ImagePicker.launchImageLibraryAsync({
      mediaTypes: ImagePicker.MediaTypeOptions.Images,
      allowsEditing: true,
      quality: 0.8,
    });

    if (!result.canceled) {
      return result.assets[0];
    }
    return null;
  };

  const pickDocument = async () => {
    const result = await DocumentPicker.getDocumentAsync({
      type: '*/*',
      copyToCacheDirectory: true,
    });

    if (result.type === 'success') {
      return result;
    }
    return null;
  };

  const uploadToSupabase = async (file: any, projectId: string) => {
    const fileExt = file.uri.split('.').pop();
    const fileName = `${projectId}/${Date.now()}.${fileExt}`;

    const { data, error } = await supabase.storage
      .from('design-uploads')
      .upload(fileName, file, {
        contentType: file.type || 'application/octet-stream',
      });

    if (error) throw error;
    return data;
  };

  return { pickImage, pickDocument, uploadToSupabase };
}
```

5. **UI Component**

```typescript
// components/FileUploadButton.tsx
import { Pressable, Text, ActivityIndicator } from 'react-native';
import { Feather } from '@expo/vector-icons';
import { useFileUpload } from '@/hooks/useFileUpload';

export function FileUploadButton({ projectId, onSuccess }) {
  const [uploading, setUploading] = useState(false);
  const { pickImage, uploadToSupabase } = useFileUpload();

  const handleUpload = async () => {
    setUploading(true);
    try {
      const file = await pickImage();
      if (file) {
        const data = await uploadToSupabase(file, projectId);
        onSuccess(data);
      }
    } catch (error) {
      Alert.alert('Upload Failed', error.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <Pressable onPress={handleUpload} disabled={uploading}>
      {uploading ? (
        <ActivityIndicator />
      ) : (
        <>
          <Feather name="upload" size={20} />
          <Text>Upload Design</Text>
        </>
      )}
    </Pressable>
  );
}
```

## Integration Points

1. **Project Detail Screen** - Add upload button in the "Files" section
2. **New Project Flow** - Allow upload during project creation
3. **Edge Function** - Already exists: `/upload-design`

## Testing Checklist

- [ ] Install required packages
- [ ] Configure app permissions in `app.json`
- [ ] Test image picker on iOS
- [ ] Test image picker on Android
- [ ] Test document picker
- [ ] Test upload to Supabase Storage
- [ ] Test with large files (>10MB)
- [ ] Test network failure scenarios
- [ ] Test progress indicators

## Estimated Effort

- **Setup & Configuration**: 1 hour
- **Implementation**: 2-3 hours
- **Testing**: 1-2 hours
- **Total**: 4-6 hours

## Priority

**Medium** - Feature is useful but not blocking for MVP usage. Admins can currently use the Supabase dashboard or provide URLs manually.

## Notes

- File upload requires testing on physical devices (not just simulators)
- Large file uploads should show progress indicators
- Consider compression for large images
- May want to add file type validation (e.g., only allow .fig, .sketch, .png, .jpg)
