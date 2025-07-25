import {computed} from "vue";

export const FEATURES_LEVELS = {
    PRODUCTION: 'production',
    DEVELOPMENT: 'development',
};

const DEFAULT_FEATURES_LEVEL = FEATURES_LEVELS.PRODUCTION;

let featuresLevel = DEFAULT_FEATURES_LEVEL;

/**
 * @param {string} level - Features level (see FEATURES_LEVELS)
 */
export function initializeFeatures(level) {
    featuresLevel = level || DEFAULT_FEATURES_LEVEL;
}

export function getFeaturesLevel() {
    return featuresLevel;
}

export function hasFeaturesLevel(featuresLevel) {
    return featuresLevel === getFeaturesLevel();
}

export function isValidFeaturesLevel(level) {
    if (!level) {
        return true;
    }

    return hasFeaturesLevel(level);
}

export const isDevFeature = computed(() => {
    return hasFeaturesLevel(FEATURES_LEVELS.DEVELOPMENT);
});
