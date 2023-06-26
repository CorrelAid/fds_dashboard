export function formatAsPercent(num,places=2) {
    return new Intl.NumberFormat('default', {
      style: 'percent',
      minimumFractionDigits: 0,
      maximumFractionDigits: places,
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

  export function formatGermanDate(date) {
    const options = {
      year: 'numeric',
      month: 'long'
    };
  
    const formattedDate = date.toLocaleString('de-DE', options);
    return formattedDate;
  }