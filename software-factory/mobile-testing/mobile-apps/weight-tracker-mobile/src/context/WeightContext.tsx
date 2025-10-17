import React, { createContext, useContext, useState, ReactNode } from 'react';

export interface WeightEntry {
  id: string;
  date: string;
  weight: number;
  bodyFat: number;
  notes?: string;
}

interface WeightContextType {
  entries: WeightEntry[];
  addEntry: (entry: Omit<WeightEntry, 'id'>) => void;
  updateEntry: (id: string, entry: Partial<WeightEntry>) => void;
  deleteEntry: (id: string) => void;
  currentWeight: number;
  currentBodyFat: number;
  goalWeight: number;
  setGoalWeight: (weight: number) => void;
}

const WeightContext = createContext<WeightContextType | undefined>(undefined);

export const useWeight = () => {
  const context = useContext(WeightContext);
  if (!context) {
    throw new Error('useWeight must be used within a WeightProvider');
  }
  return context;
};

// Sample data
const initialEntries: WeightEntry[] = [
  { id: '1', date: '2025-09-15', weight: 185.2, bodyFat: 15.2 },
  { id: '2', date: '2025-09-16', weight: 184.8, bodyFat: 15.1 },
  { id: '3', date: '2025-09-17', weight: 184.5, bodyFat: 15.0 },
  { id: '4', date: '2025-09-18', weight: 184.2, bodyFat: 14.9 },
  { id: '5', date: '2025-09-19', weight: 183.9, bodyFat: 14.8 },
  { id: '6', date: '2025-09-20', weight: 183.6, bodyFat: 14.7 },
  { id: '7', date: '2025-09-21', weight: 183.3, bodyFat: 14.6 },
  { id: '8', date: '2025-09-22', weight: 183.0, bodyFat: 14.5 },
  { id: '9', date: '2025-09-23', weight: 182.7, bodyFat: 14.4 },
  { id: '10', date: '2025-09-24', weight: 182.4, bodyFat: 14.3 },
  { id: '11', date: '2025-09-25', weight: 182.1, bodyFat: 14.2 },
  { id: '12', date: '2025-09-26', weight: 181.8, bodyFat: 14.1 },
  { id: '13', date: '2025-09-27', weight: 181.5, bodyFat: 14.0 },
  { id: '14', date: '2025-09-28', weight: 181.2, bodyFat: 13.9 },
  { id: '15', date: '2025-09-29', weight: 180.9, bodyFat: 13.8 },
  { id: '16', date: '2025-09-30', weight: 180.6, bodyFat: 13.7 },
  { id: '17', date: '2025-10-01', weight: 180.3, bodyFat: 13.6 },
  { id: '18', date: '2025-10-02', weight: 180.0, bodyFat: 13.5 },
  { id: '19', date: '2025-10-03', weight: 179.7, bodyFat: 13.4 },
  { id: '20', date: '2025-10-04', weight: 179.4, bodyFat: 13.3 },
  { id: '21', date: '2025-10-05', weight: 179.1, bodyFat: 13.2 },
  { id: '22', date: '2025-10-06', weight: 178.8, bodyFat: 13.1 },
  { id: '23', date: '2025-10-07', weight: 178.5, bodyFat: 13.0 },
  { id: '24', date: '2025-10-08', weight: 178.2, bodyFat: 12.9 },
  { id: '25', date: '2025-10-09', weight: 178.4, bodyFat: 12.8 },
  { id: '26', date: '2025-10-10', weight: 178.1, bodyFat: 12.7 },
  { id: '27', date: '2025-10-11', weight: 177.8, bodyFat: 12.6 },
  { id: '28', date: '2025-10-12', weight: 177.5, bodyFat: 12.5 },
  { id: '29', date: '2025-10-13', weight: 177.2, bodyFat: 12.4 },
  { id: '30', date: '2025-10-14', weight: 178.4, bodyFat: 12.8 },
];

export const WeightProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [entries, setEntries] = useState<WeightEntry[]>(initialEntries);
  const [goalWeight, setGoalWeight] = useState(175.0);

  const addEntry = (entry: Omit<WeightEntry, 'id'>) => {
    const newEntry: WeightEntry = {
      ...entry,
      id: Date.now().toString(),
    };
    setEntries(prev => [...prev, newEntry].sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime()));
  };

  const updateEntry = (id: string, updatedEntry: Partial<WeightEntry>) => {
    setEntries(prev => prev.map(entry => 
      entry.id === id ? { ...entry, ...updatedEntry } : entry
    ));
  };

  const deleteEntry = (id: string) => {
    setEntries(prev => prev.filter(entry => entry.id !== id));
  };

  const currentWeight = entries[entries.length - 1]?.weight || 0;
  const currentBodyFat = entries[entries.length - 1]?.bodyFat || 0;

  const value: WeightContextType = {
    entries,
    addEntry,
    updateEntry,
    deleteEntry,
    currentWeight,
    currentBodyFat,
    goalWeight,
    setGoalWeight,
  };

  return (
    <WeightContext.Provider value={value}>
      {children}
    </WeightContext.Provider>
  );
};
