export const staffRanges = [
    '1-10',
    '10-50',
    '50-200',
    '200-500',
    '500-1K',
    '1K-5K',
    '5K-10K',
    '> 10K'
];

export const getStaffRangeColor = (staffRange) => {
    switch (staffRange) {
        case '1-10':
            return 'orange';
        case '10-50':
            return 'green';
        case '50-200':
            return 'blue';
        case '200-500':
            return 'pink';
        case '500-1K':
            return 'purple';
        case '1K-5K':
            return 'purple';
        case '5K-10K':
            return 'purple';
        case '> 10K':
            return 'purple';
        default:
            return 'grey';
    }
}; 