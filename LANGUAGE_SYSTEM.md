# Language Toggle System Documentation

## Overview
PenzFlow now supports bilingual interface switching between English and Indonesian. This feature allows users to easily switch languages without losing their session data.

## Features Implemented

### 1. Language Toggle Widget
- **Location**: Available on both login page and main application header
- **Options**: 🇮🇩 Bahasa Indonesia / 🇺🇸 English
- **Default**: Indonesian (since most users prefer Indonesian)
- **Persistence**: Language preference is saved in session state

### 2. Translation System
- **File**: `src/utils/translations.py`
- **Coverage**: 150+ translation keys covering all major UI elements
- **Languages**: English (en) and Indonesian (id)
- **Structure**: Organized by functional areas (general, navigation, products, sales, etc.)

### 3. Usage in Code
```python
from utils.translations import t

# Use the t() function to get translated text
st.header(f"📦 {t('products')}")
st.button(t('save'))
st.selectbox(t('category'), options)
```

## Key Translation Areas

### Navigation & General
- Dashboard, menu items, buttons
- Login/logout messages
- Success/error messages
- Common actions (save, cancel, edit, delete)

### Business Functions
- Product management (variants, pricing, categories)
- Customer management
- Sales operations
- Field sales activities
- Reports and analytics

### FMCG-Specific Terms
- Product variants (sizes, volumes)
- Tiered pricing
- Bulk quantities
- Stock management

## How It Works

### 1. Language Initialization
```python
from utils.translations import init_language
init_language()  # Sets default to Indonesian
```

### 2. Language Toggle (Located in Settings)
- Navigate to Settings page to change language
- Dropdown widget updates session state
- Page automatically refreshes when language changes
- All translated elements update immediately
- Language indicator shown in sidebar for quick reference

### 3. Translation Function
```python
def t(key):
    current_lang = get_current_language()
    return get_text(key, current_lang)
```

## Adding New Translations

### 1. Add to Translation Dictionary
```python
TRANSLATIONS = {
    'en': {
        'new_feature': 'New Feature',
        # ... other translations
    },
    'id': {
        'new_feature': 'Fitur Baru',
        # ... other translations
    }
}
```

### 2. Use in Code
```python
st.header(t('new_feature'))
```

## Best Practices

### 1. Translation Keys
- Use descriptive, lowercase keys with underscores
- Group related translations (e.g., `product_name`, `product_code`)
- Keep keys consistent across the application

### 2. UI Implementation
- Always use `t()` function for user-facing text
- Maintain UI layout consistency across languages
- Test both languages for text length differences

### 3. Business Context
- Indonesian terms are preferred for local business processes
- English technical terms are kept where commonly used
- Currency and date formats remain consistent (Indonesian standards)

## Current Status

### ✅ Implemented
- Core translation system
- Language toggle widget
- Main navigation translation
- Product management page translation
- Login/logout flow translation

### 🔄 In Progress
- Complete translation of all pages
- Business-specific terminology refinement
- User preference persistence across sessions

### 🎯 Future Enhancements
- Add more languages (e.g., Javanese for regional users)
- Right-to-left text support if needed
- Context-sensitive translations
- Translation management interface

## User Experience

### Default Behavior
1. Application loads in Indonesian by default
2. Users can switch to English using the dropdown
3. Language preference persists during the session
4. All interface elements update immediately

### Accessibility
- Clear language indicators (flags + text)
- Consistent toggle location across pages
- No data loss when switching languages
- Intuitive language selection

## Technical Benefits

1. **Easy Maintenance**: Centralized translation management
2. **Scalability**: Easy to add new languages
3. **Performance**: Minimal overhead with session-based caching
4. **Flexibility**: Granular control over translated elements
5. **Consistency**: Unified translation function across all pages

This language system makes PenzFlow more accessible to Indonesian users while maintaining international usability for English speakers.
