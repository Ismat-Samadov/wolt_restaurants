# 💰 Tip Calculator

A responsive, mobile-friendly tip calculator built with Next.js and Tailwind CSS. Perfect for restaurant goers and travelers who need to calculate tips and split bills easily.

## Features

- 🧮 **Easy Tip Calculation**: Calculate tips with preset percentages (15%, 18%, 20%, 22%, 25%) or custom percentages
- 👥 **Bill Splitting**: Split the total bill among multiple people
- 📱 **Mobile-Friendly**: Fully responsive design that works great on all devices
- 🎨 **Intuitive UI**: Clean, attractive design with smooth interactions
- 🚀 **Fast Performance**: Built with Next.js for optimal performance
- 🔍 **SEO Optimized**: Includes meta tags, structured data, and proper semantic HTML

## Technologies Used

- **Framework**: Next.js 15.4.6 with App Router
- **Styling**: Tailwind CSS
- **Language**: TypeScript
- **Deployment**: Vercel

## Getting Started

### Prerequisites

- Node.js 18 or later
- npm or yarn

### Installation

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd tipcalculator
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm run dev
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

## Deployment

### Deploy to Vercel

1. Push your code to GitHub
2. Connect your repository to Vercel
3. Vercel will automatically deploy your app

Or use the Vercel CLI:

```bash
npm install -g vercel
vercel
```

### Manual Deployment

1. Build the application:
   ```bash
   npm run build
   ```

2. Start the production server:
   ```bash
   npm start
   ```

## Project Structure

```
src/
├── app/
│   ├── layout.tsx          # Root layout with SEO metadata
│   ├── page.tsx            # Main tip calculator component
│   └── globals.css         # Global styles
└── ...
```

## Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run start` - Start production server
- `npm run lint` - Run ESLint

## Features in Detail

### Tip Calculation
- Enter bill amount
- Select from preset tip percentages or enter custom percentage
- Automatic calculation of tip amount and total

### Bill Splitting
- Adjust number of people using +/- buttons or direct input
- Automatic calculation of per-person amount
- Minimum of 1 person enforced

### User Experience
- Real-time calculations as you type
- Clear all functionality to reset form
- Visual feedback for selected tip percentage
- Mobile-optimized touch targets

### SEO Features
- Semantic HTML structure
- Meta tags for social sharing
- Structured data for search engines
- Optimized for search terms like "tip calculator" and "bill splitter"

## License

This project is open source and available under the [MIT License](LICENSE).
