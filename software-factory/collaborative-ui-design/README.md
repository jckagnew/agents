# 🎨 Collaborative UI Design App

A sophisticated UI design collaboration platform that allows you to work with clients and development partners on UI design, then seamlessly feed the results into the software factory for app generation.

## 🚀 Features

### **Core Design Tools**
- **Drag & Drop Canvas**: Intuitive design interface with React Flow
- **Component Library**: Pre-built UI components with variants
- **Real-time Properties**: Live editing of component properties
- **Design System**: Consistent tokens and styling
- **Grid & Snap**: Precise alignment and positioning

### **Collaboration Features**
- **Real-time Collaboration**: Multiple users can work simultaneously
- **Comment System**: Contextual feedback on specific elements
- **Version Control**: Track design iterations and changes
- **Client Review**: Easy sharing and approval workflows

### **Export & Integration**
- **React Components**: Generate production-ready React code
- **Software Factory Integration**: Seamless handoff to app generation
- **Multiple Formats**: Export to HTML, CSS, Figma, and more
- **Asset Management**: Optimized images and icons

## 🛠️ Technology Stack

- **Frontend**: React 18 + TypeScript
- **State Management**: Zustand
- **Canvas**: React Flow
- **Styling**: Tailwind CSS
- **Icons**: Lucide React
- **Animations**: Framer Motion

## 🚀 Getting Started

### **Prerequisites**
- Node.js 16+ 
- npm or yarn

### **Installation**

1. **Clone and install dependencies:**
   ```bash
   cd software-factory/collaborative-ui-design
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm start
   ```

3. **Open your browser:**
   Navigate to `http://localhost:3000`

## 🎯 Usage

### **Solo Mode**
1. **Create a new project** or open existing
2. **Drag components** from the library to the canvas
3. **Edit properties** in the properties panel
4. **Export** to React components or other formats

### **Collaboration Mode**
1. **Invite collaborators** via email
2. **Share project** with clients for review
3. **Collect feedback** through comments and annotations
4. **Approve designs** through workflow system

### **Export to Software Factory**
1. **Design your UI** using the canvas
2. **Export as React components**
3. **Import into Software Factory**
4. **Generate universal apps** (iOS, Android, Web)

## 📁 Project Structure

```
src/
├── components/
│   ├── Canvas/           # Design canvas components
│   ├── Library/          # Component library
│   ├── Properties/       # Properties panel
│   └── Layout/           # Layout components
├── stores/               # Zustand state management
├── types/                # TypeScript type definitions
├── utils/                # Utility functions
└── hooks/                # Custom React hooks
```

## 🎨 Component Library

### **Available Components**
- **Atoms**: Button, Text, Input, Image
- **Molecules**: Card, Form, Navigation
- **Organisms**: Header, Footer, Sidebar
- **Templates**: Page layouts, Dashboard
- **Layout**: Container, Grid, Flexbox

### **Custom Components**
- Create your own components
- Define properties and variants
- Generate React code automatically
- Share with team members

## 🔧 Development

### **Adding New Components**

1. **Define component structure:**
   ```typescript
   const newComponent: ComponentDefinition = {
     id: 'my-component',
     name: 'My Component',
     category: 'atom',
     properties: [...],
     variants: [...],
     code: { react: '...', css: '...' }
   };
   ```

2. **Add to component library:**
   ```typescript
   loadComponentLibrary([...existingComponents, newComponent]);
   ```

3. **Create renderer in ComponentNode.tsx**

### **Customizing the Canvas**

- **Grid settings**: Modify grid size and appearance
- **Snap behavior**: Adjust snap-to-grid sensitivity
- **Zoom controls**: Customize zoom limits and steps
- **Selection**: Modify selection behavior and appearance

## 🚀 Deployment

### **Production Build**
```bash
npm run build
```

### **Docker Deployment**
```bash
docker build -t collaborative-ui-design .
docker run -p 3000:3000 collaborative-ui-design
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is part of the Software Factory ecosystem and follows the same licensing terms.

## 🆘 Support

For support and questions:
- Check the documentation
- Open an issue on GitHub
- Contact the development team

---

**Built with ❤️ for the Software Factory ecosystem**