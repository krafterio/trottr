import { createContext } from "reka-ui";

// Define the TiptapContext type

// Create context for Tiptap components
export const [useTiptapContext, provideTiptapContext] =
  createContext("TiptapEditor");

export { default as TiptapContent } from "./TiptapContent.vue";
// Export all component parts
export { default as TiptapEditor } from "./TiptapEditor.vue";
export { default as TiptapIcon } from "./TiptapIcon.vue";
export { default as TiptapKeyboardShortcuts } from "./TiptapKeyboardShortcuts.vue";
export { default as TiptapMobileToolbar } from "./TiptapMobileToolbar.vue";
export { default as TiptapProvider } from "./TiptapProvider.vue";
export { default as TiptapSlotPanel } from "./TiptapSlotPanel.vue";
export { default as TiptapStatusBar } from "./TiptapStatusBar.vue";
export { default as TiptapTableToolbar } from "./TiptapTableToolbar.vue";
export { default as TiptapToolbar } from "./TiptapToolbar.vue";

export { default as TiptapTreeItem } from "./TiptapTreeItem.vue";
// Export the tree-based structure components
export { default as TiptapTreeStructure } from "./TiptapTreeStructure.vue";

// Re-export utilities
export * from "./tiptapTreeUtils";
