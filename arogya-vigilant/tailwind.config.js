/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                hcblue: { // Healthcare Blue
                    900: '#0B2042',
                    800: '#0F2C59', // Primary
                    700: '#173E7A'
                },
                teals: {
                    600: '#006666',
                    500: '#008080', // Accent
                    400: '#339999'
                },
                danger: {
                    900: '#7F1D1D',
                    800: '#991B1B',
                    700: '#B91C1C', // Action Danger
                },
                offwhite: '#F8FAFC' // Soft background
            },
            fontFamily: {
                sans: ['Inter', 'system-ui', 'sans-serif'],
            },
        },
    },
    plugins: [],
}
