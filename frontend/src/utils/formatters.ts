export const formatTime = (timestamp: string, includeSeconds: boolean = false): string => {
  const date = new Date(timestamp);
  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');

  if (includeSeconds) {
    const seconds = date.getSeconds().toString().padStart(2, '0');
    return `${hours}:${minutes}:${seconds}`;
  }

  return `${hours}:${minutes}`;
};

export const formatPrice = (price: number): string => {
  return price.toFixed(2);
};

export const formatDate = (timestamp: string): string => {
  const date = new Date(timestamp);
  return date.toLocaleDateString();
};