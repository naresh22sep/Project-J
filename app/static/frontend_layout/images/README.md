# Image Assets for Frontend Layout

This directory contains images for the frontend layout used by JobSeeker and Consultancy modules.

## Recommended Images:

### Hero Section:
- hero-bg.jpg (1920x1080) - Background image for hero sections
- hero-jobseeker.jpg (800x600) - Job seeker hero image
- hero-consultancy.jpg (800x600) - Consultancy hero image

### UI Elements:
- logo.png (200x50) - Main application logo
- logo-white.png (200x50) - White version of logo for dark backgrounds
- favicon.ico (32x32) - Browser favicon
- avatar-placeholder.png (150x150) - Default user avatar

### Feature Images:
- feature-search.jpg (300x200) - Job search feature
- feature-apply.jpg (300x200) - Job application feature
- feature-profile.jpg (300x200) - Profile management feature
- feature-match.jpg (300x200) - Job matching feature

### Company Logos:
- company-placeholder.png (100x100) - Default company logo
- partner-logos/ - Directory for partner company logos

### Icons:
- icon-jobseeker.svg - Job seeker icon
- icon-consultancy.svg - Consultancy icon
- icon-job.svg - Job icon
- icon-application.svg - Application icon

## Usage:
Reference these images in templates using:
```html
<img src="{{ url_for('static', filename='frontend_layout/images/image-name.jpg') }}" alt="Description">
```

## File Formats:
- Use JPG for photographs and complex images
- Use PNG for logos and images with transparency
- Use SVG for scalable icons and simple graphics
- Use WebP for optimized loading (with fallbacks)