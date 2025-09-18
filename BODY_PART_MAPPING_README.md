# 🎯 Body Part Mapping Parsers

This repository contains enhanced body part mapping parsers that extract and format avatar body part information from Roblox 3D models in different formats.

## 📋 Available Parsers

### 1. 🔧 Enhanced Body Part Mapping Parser (`body_part_mapping_parser.py`)
**Rich, detailed analysis with comprehensive metadata**

Features:
- ✅ Complete avatar profile information (verification status, account creation date)
- ✅ Detailed avatar configuration (body colors, scales, worn items)
- ✅ 3D model structure analysis
- ✅ Enhanced visual formatting with colors and emojis
- ✅ Comprehensive usage guides for 3D software and game engines
- ✅ Statistical analysis and complexity metrics
- ✅ File integrity information

**Output:** `ENHANCED_BODY_PART_MAPPING.txt` (~14KB)

### 2. 🎯 Simple Body Part Mapping Parser (`simple_body_part_mapper.py`)
**Clean, focused output with essential information only**

Features:
- ✅ Clean body part mapping table
- ✅ Color-coded visualization
- ✅ Sorted by anatomical structure
- ✅ Compact format for quick reference
- ✅ Essential statistics only

**Output:** `SIMPLE_BODY_PART_MAPPING.txt` (~3KB)

### 3. 📚 Body Part Mapping Examples (`body_part_mapping_examples.py`)
**Demonstration script showing both parsers in action**

Features:
- ✅ Automatic package discovery
- ✅ Runs both parsers simultaneously
- ✅ File size comparison
- ✅ Usage examples and analysis

## 🚀 Quick Start

### Run Enhanced Parser
```bash
python body_part_mapping_parser.py
```

### Run Simple Parser
```bash
python simple_body_part_mapper.py
```

### Run Examples & Comparison
```bash
python body_part_mapping_examples.py
```

## 📊 Parser Comparison

| Feature | Enhanced | Simple | Original |
|---------|----------|---------|----------|
| File Size | ~14KB | ~3KB | ~6KB |
| Avatar Profile Info | ✅ | ❌ | ❌ |
| Body Colors | ✅ | ❌ | ❌ |
| Worn Items | ✅ | ❌ | ❌ |
| Usage Guides | ✅ | ❌ | ✅ |
| Statistical Analysis | ✅ | ✅ | ✅ |
| Clean Format | ❌ | ✅ | ❌ |

## 🎨 Body Part Color Guide

The parsers use color-coded emojis to categorize different body parts:

- 🟡 **Head/Face**: Player1
- 🟢 **Torso**: Player2 (Front), Player9 (Back)  
- 🔵🔷🟦 **Arms & Hands**: Player3-8 (Upper arms, lower arms, hands)
- 🟣🟪🟫 **Legs & Feet**: Player10-15 (Upper legs, lower legs, feet)
- ⭐ **Accessory Handle**: Handle1 (Tool/weapon attachment point)

## 📁 Output Files

### Enhanced Parser Output Structure
```
ENHANCED_BODY_PART_MAPPING.txt
├── 🎭 Avatar Profile Information
├── 🎨 Avatar Configuration (colors, items, scales)
├── 🏗️ 3D Model Structure Info
├── 🎯 Body Part Attachment Points (detailed)
├── 🛠️ Comprehensive Usage Guide
├── 📊 Advanced Statistical Analysis
└── 📄 File Information & Metadata
```

### Simple Parser Output Structure
```
SIMPLE_BODY_PART_MAPPING.txt
├── 🎯 User Header (ID & Username)
├── 📋 Clean Body Part Mapping Table
├── 🎨 Color Guide Reference
├── 📊 Quick Statistics
└── 🕒 Generation Info
```

## 🛠️ Usage in Development

### Blender Integration
```python
# Enhanced parser provides detailed asset information
# Simple parser provides clean group reference
# Both include line numbers for OBJ file navigation
```

### Unity/Unreal Engine
```csharp
// Use body part mapping for:
// - Collision detection setup
// - Attachment point configuration
// - Dynamic avatar customization
```

### Web Development (Three.js)
```javascript
// Parse mapping files to:
// - Create interactive avatar viewers
// - Implement real-time customization
// - Handle attachment point logic
```

## 📈 Performance

| Parser | Processing Time | Memory Usage | Output Quality |
|--------|----------------|---------------|----------------|
| Enhanced | ~2-3 seconds | High | Comprehensive |
| Simple | ~1 second | Low | Essential |

## 🎯 Use Cases

### Enhanced Parser - Best for:
- 📚 Research and analysis projects
- 🎮 Game development with detailed avatar systems
- 🔧 Complete avatar reconstruction
- 📊 Avatar database creation

### Simple Parser - Best for:
- 🚀 Quick reference during development
- 📱 Mobile applications with size constraints  
- 🔄 Automated processing pipelines
- 📋 Documentation and tutorials

## 📋 Requirements

```txt
requests>=2.28.0
pathlib2>=2.3.7; python_version < "3.4"
```

## 🔧 Installation

1. Clone the repository
2. Install requirements: `pip install -r requirements.txt`
3. Run any parser script

## 🐛 Troubleshooting

### Common Issues:
1. **"Package not found"** - Ensure avatar package exists in `final_integrated/` directory
2. **"Import error"** - Make sure both parser files are in the same directory
3. **"JSON parsing error"** - Verify avatar package integrity

### File Structure Required:
```
your-project/
├── body_part_mapping_parser.py
├── simple_body_part_mapper.py
├── body_part_mapping_examples.py
└── final_integrated/
    └── username_userid/
        └── COMPLETE_AVATAR_PACKAGE.json
```

## 🎉 Examples

Generated files can be found in the avatar package directory:
- `ENHANCED_BODY_PART_MAPPING.txt` - Rich, detailed analysis
- `SIMPLE_BODY_PART_MAPPING.txt` - Clean, focused mapping

Both files are perfectly formatted for:
- ✅ Easy reading in text editors
- ✅ Import into documentation
- ✅ Reference during development
- ✅ Integration with development tools

---

**Generated by Enhanced Body Part Mapping Parser v2.0**  
🏠 [Repository](https://github.com/Mino-is-me/Roblox-hook) | 📧 [Issues](https://github.com/Mino-is-me/Roblox-hook/issues)