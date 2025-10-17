/**
 * Date Utility Service - Web Version (Next.js)
 * Handles date conversion and formatting for US users
 * 
 * Usage:
 * import { dateUtilityService } from '@/services/DateUtilityService';
 * 
 * const usDate = dateUtilityService.formatToUSDate('2024-01-15');
 * const isoDate = dateUtilityService.parseFromUSDate('01/15/2024');
 */

class DateUtilityService {
  /**
   * Convert ISO date string (YYYY-MM-DD) to US format (MM/DD/YYYY)
   */
  formatToUSDate(isoDate: string): string {
    try {
      if (!isoDate) return '';
      
      const date = new Date(isoDate + 'T00:00:00'); // Ensure local timezone
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const day = date.getDate().toString().padStart(2, '0');
      const year = date.getFullYear();
      
      return `${month}/${day}/${year}`;
    } catch (error) {
      console.error('Date formatting error:', error);
      return isoDate; // Return original if formatting fails
    }
  }

  /**
   * Convert US date string (MM/DD/YYYY) to ISO format (YYYY-MM-DD)
   */
  parseFromUSDate(usDate: string): string {
    try {
      if (!usDate) return '';
      
      // Handle MM/DD/YYYY format
      const parts = usDate.split('/');
      if (parts.length === 3) {
        const month = parts[0].padStart(2, '0');
        const day = parts[1].padStart(2, '0');
        const year = parts[2];
        
        // Validate date
        const date = new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
        if (isNaN(date.getTime())) {
          throw new Error('Invalid date');
        }
        
        return `${year}-${month}-${day}`;
      }
      
      throw new Error('Invalid date format');
    } catch (error) {
      console.error('Date parsing error:', error);
      return usDate; // Return original if parsing fails
    }
  }

  /**
   * Get today's date in ISO format
   */
  getTodayISO(): string {
    const today = new Date();
    const year = today.getFullYear();
    const month = (today.getMonth() + 1).toString().padStart(2, '0');
    const day = today.getDate().toString().padStart(2, '0');
    
    return `${year}-${month}-${day}`;
  }

  /**
   * Get today's date in US format
   */
  getTodayUS(): string {
    return this.formatToUSDate(this.getTodayISO());
  }

  /**
   * Format date for display with day of week
   */
  formatWithDayOfWeek(isoDate: string): string {
    try {
      const date = new Date(isoDate + 'T00:00:00');
      const dayNames = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
      const dayName = dayNames[date.getDay()];
      const usDate = this.formatToUSDate(isoDate);
      
      return `${dayName}, ${usDate}`;
    } catch (error) {
      console.error('Date formatting with day error:', error);
      return this.formatToUSDate(isoDate);
    }
  }

  /**
   * Format date for input placeholder
   */
  getInputPlaceholder(): string {
    return 'MM/DD/YYYY';
  }

  /**
   * Validate US date format
   */
  isValidUSDate(usDate: string): boolean {
    try {
      const isoDate = this.parseFromUSDate(usDate);
      const date = new Date(isoDate + 'T00:00:00');
      return !isNaN(date.getTime());
    } catch {
      return false;
    }
  }

  /**
   * Get relative date description (Today, Yesterday, etc.)
   */
  getRelativeDateDescription(isoDate: string): string {
    try {
      const date = new Date(isoDate + 'T00:00:00');
      const today = new Date();
      const yesterday = new Date(today);
      yesterday.setDate(today.getDate() - 1);
      
      // Reset time to compare dates only
      date.setHours(0, 0, 0, 0);
      today.setHours(0, 0, 0, 0);
      yesterday.setHours(0, 0, 0, 0);
      
      if (date.getTime() === today.getTime()) {
        return 'Today';
      } else if (date.getTime() === yesterday.getTime()) {
        return 'Yesterday';
      } else {
        return this.formatToUSDate(isoDate);
      }
    } catch (error) {
      console.error('Relative date error:', error);
      return this.formatToUSDate(isoDate);
    }
  }

  /**
   * Sort dates in descending order (newest first)
   */
  sortDatesDescending(dates: string[]): string[] {
    return [...dates].sort((a, b) => b.localeCompare(a));
  }

  /**
   * Get date range for last N days
   */
  getLastNDays(n: number): string[] {
    const dates: string[] = [];
    const today = new Date();
    
    for (let i = 0; i < n; i++) {
      const date = new Date(today);
      date.setDate(today.getDate() - i);
      
      const year = date.getFullYear();
      const month = (date.getMonth() + 1).toString().padStart(2, '0');
      const day = date.getDate().toString().padStart(2, '0');
      
      dates.push(`${year}-${month}-${day}`);
    }
    
    return dates;
  }
}

export const dateUtilityService = new DateUtilityService();
