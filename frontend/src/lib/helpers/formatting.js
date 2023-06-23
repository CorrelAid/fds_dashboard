export function formatAsPercent(num) {
    return new Intl.NumberFormat('default', {
      style: 'percent',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(num / 100);
  }

  export function formatCosts(num) {
    return new Intl.NumberFormat('default', {
      style: 'currency',
      currency: 'EUR',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(num).replace(',', '.');
  }

  export function roundNumber(num, decimalPlaces) {
    const factor = 10 ** decimalPlaces;
    return Math.round(num * factor) / factor;
  }