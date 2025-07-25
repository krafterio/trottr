export const usePreview = () => {
    const isPreviewMode = import.meta.env.VITE_MODE_PREVIEW === 'True';

    return {
        isPreviewMode
    };
} 
