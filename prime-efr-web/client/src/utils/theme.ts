export const readCssVariable = (variableName: string, fallback = ''): string => {
  if (typeof window === 'undefined') {
    return fallback;
  }
  const value = getComputedStyle(document.documentElement).getPropertyValue(variableName);
  return value?.trim() || fallback;
};

export const getChartPalette = (length = 8): string[] => {
  const palette: string[] = [];
  for (let index = 1; index <= length; index += 1) {
    const tokenName = `--color-chart-categorical-${index}` as const;
    palette.push(readCssVariable(tokenName, 'var(--color-primary)'));
  }
  return palette;
};
