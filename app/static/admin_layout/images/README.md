# Image Assets for Admin Layout

This directory contains images for the admin layout used by Admin and SuperAdmin modules.

## Recommended Images:

### Dashboard:
- dashboard-bg.jpg (1920x1080) - Admin dashboard background
- admin-avatar.png (150x150) - Default admin avatar
- superadmin-avatar.png (150x150) - Default super admin avatar

### Icons:
- icon-users.svg - Users management icon
- icon-jobs.svg - Jobs management icon
- icon-applications.svg - Applications management icon
- icon-analytics.svg - Analytics icon
- icon-settings.svg - Settings icon
- icon-reports.svg - Reports icon

### Charts and Graphics:
- chart-placeholder.png (400x300) - Placeholder for chart areas
- graph-bg.png (800x400) - Background for graph areas
- stats-bg.png (300x200) - Background for statistics cards

### Status Icons:
- status-active.svg - Active status icon
- status-inactive.svg - Inactive status icon
- status-pending.svg - Pending status icon
- status-approved.svg - Approved status icon
- status-rejected.svg - Rejected status icon

### Admin UI:
- admin-logo.png (150x40) - Admin panel logo
- login-bg.jpg (1920x1080) - Admin login background
- sidebar-bg.jpg (300x1080) - Sidebar background pattern

### File Type Icons:
- icon-pdf.svg - PDF file icon
- icon-doc.svg - Document file icon
- icon-excel.svg - Excel file icon
- icon-image.svg - Image file icon

## Usage:
Reference these images in admin templates using:
```html
<img src="{{ url_for('static', filename='admin_layout/images/image-name.jpg') }}" alt="Description">
```

## File Formats:
- Use JPG for photographs and backgrounds
- Use PNG for logos and images with transparency  
- Use SVG for scalable icons and admin graphics
- Keep file sizes optimized for fast admin panel loading

## Admin Theme Colors:
- Primary: #007bff
- Secondary: #6c757d  
- Success: #28a745
- Danger: #dc3545
- Warning: #ffc107
- Info: #17a2b8
- Dark: #343a40
- Light: #f8f9fa