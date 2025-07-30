import {useMetadataStore} from "@/common/stores/metadata";

export const FILTER_CONDITIONS = [
    '&',
    '|',
];

export const FILTER_OPERATORS = {
    '=': 'Egal',
    '!=': 'Différent',
    '>': 'Supérieur',
    '>=': 'Supérieur ou égal',
    '<': 'Inférieur',
    '<=': 'Inférieur ou égal',
    'starts with': 'Commence par',
    'ends with': 'Finit par',
    'not starts with': 'Ne commence pas par',
    'not ends with': 'Ne finit pas par',
    'icontains': 'Contient',
    'not icontains': 'Ne contient pas',
    'is true': 'Est vrai',
    'is false': 'Est faux',
    'is empty': 'Est vide',
    'is not empty': 'N\'est pas vide',
};

export const NO_VALUE_FILTERS = [
    'is true',
    'is false',
    'is empty',
    'is not empty',
];

export function useFilters() {
    const metadataStore = useMetadataStore();

    return {
        isFilter,
        isCondition,
        isRule,
        createCondition,
        createRule,
        normalize,
        normalizeJson: async (modelName, filter) => await validateJson(metadataStore, modelName, filter),
        merge: async (modelName, ...filters) => await merge(metadataStore, modelName, ...filters),
        mergeJson: async (modelName, ...filters) => await mergeJson(metadataStore, modelName, ...filters),
        validate: async (modelName, filter) => await validate(metadataStore, modelName, filter),
        validateJson: async (modelName, filter) => await validateJson(metadataStore, modelName, filter),
    }
}

function isCondition(filter) {
    return Array.isArray(filter)
        && filter.length === 2
        && typeof filter[0] === 'string'
        && FILTER_CONDITIONS.includes(filter[0])
        && Array.isArray(filter[1])
    ;
}

function isRule(filter) {
    return !isCondition(filter)
        && Array.isArray(filter)
        && filter.length >= 2
        && typeof filter[0] === 'string'
        && typeof filter[1] === 'string'
    ;
}

function createCondition(condition = '&', rules = []) {
    return [condition, rules];
}

function createRule(field = '', operator = '', value = undefined) {
    const rule = [field, operator];

    if (value !== undefined) {
        rule.push(value);
    }

    return rule;
}

function isFilter(filter) {
    return isCondition(filter) || isRule(filter);
}

function normalize(filter) {
    filter = normalizeFilter(filter);

    return simplifyFilter(filter);
}

function normalizeFilter(filter) {
    if (isCondition(filter)) {
        return filter;
    }

    if (isRule(filter)) {
        return filter;
    }

    if (Array.isArray(filter)) {
        const newFilter = [];

        filter.forEach((item, index) => {
            const normalized = normalizeFilter(item)

            if (normalized) {
                newFilter.push(normalized);
            }
        });

        if (newFilter.length > 0) {
            return ['&', newFilter];
        }

        return null;
    }

    return null;
}

function simplifyFilter(filter) {
    if (filter
        && Array.isArray(filter)
        && filter.length === 2
        && ['&', '|'].includes(filter[0])
        && Array.isArray(filter[1])
        && filter[1].length === 1
        && !isCondition(filter[1][0])
    ) {
        filter = filter[1][0];
    }

    return filter;
}

async function validate(metadataStore, modelName, filter) {
    const metadata = await metadataStore.getMetadata(modelName);

    if (!metadata) {
        return null;
    }

    filter = normalize(filter);

    if (!filter) {
        return null;
    }

    return validateFilter(metadataStore, metadata, filter);
}

async function validateJson(metadataStore, modelName, filter) {
    const res = await validate(metadataStore, modelName, filter);

    return res ? JSON.stringify(res) : null;
}

async function validateFilter(metadataStore, metadata, filter) {
    if (isCondition(filter)) {
        return await validateCondition(metadataStore, metadata, filter);
    }

    if (isRule(filter)) {
        return await validateRule(metadataStore, metadata, filter);
    }

    return null;
}

async function validateCondition(metadataStore, metadata, condition) {
    const operator = condition[0];
    const filters = condition[1];
    const validatedFilters = [];

    for (const filter of filters) {
        const validatedFilter = await validateFilter(metadataStore, metadata, filter);

        if (validatedFilter) {
            validatedFilters.push(validatedFilter);
        }
    }

    if (validatedFilters.length === 0) {
        return null;
    }

    if (validatedFilters.length === 1) {
        return validatedFilters[0];
    }

    return [operator, validatedFilters];
}

async function validateRule(metadataStore, metadata, rule) {
    const fieldPath = rule[0];
    const operator = rule[1];

    if (fieldPath.includes('.')) {
        return await validateRelationRule(metadataStore, metadata, rule);
    }

    if (!metadata.fields[fieldPath]) {
        return null;
    }

    const field = metadata.fields[fieldPath];

    if (!field.filter_operators.includes(operator)) {
        return null;
    }

    return rule;
}

async function validateRelationRule(metadataStore, metadata, rule) {
    const fieldPath = rule[0];
    const parts = fieldPath.split('.');
    const relationField = parts[0];
    const subField = parts.slice(1).join('.');

    if (!metadata.fields[relationField]) {
        return null;
    }

    const field = metadata.fields[relationField];

    if (!field.target) {
        return null;
    }

    const targetMetadata = await metadataStore.getMetadata(field.target);

    if (!targetMetadata) {
        return null;
    }

    const subRule = [subField, rule[1]];

    if (rule.length > 2) {
        subRule.push(rule[2]);
    }

    const validatedSubRule = await validateRule(metadataStore, targetMetadata, subRule);

    if (!validatedSubRule) {
        return null;
    }

    return [fieldPath, rule[1], rule.length > 2 ? rule[2] : null].filter(item => item !== null);
}

async function merge(metadataStore, modelName, ...filters) {
    const validFilters = [];

    for (const filter of filters) {
        const validFilter = await validate(metadataStore, modelName, filter);

        if (validFilter) {
            validFilters.push(validFilter);
        }
    }

    if (validFilters.length === 0) {
        return null;
    }

    return normalize(['&', validFilters]);
}

async function mergeJson(metadataStore, modelName, ...filters) {
    const res = await merge(metadataStore, modelName, ...filters);

    return res ? JSON.stringify(res) : null;
}
