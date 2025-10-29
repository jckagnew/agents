import { beforeAll, afterAll, beforeEach, afterEach } from 'vitest'
import { vi } from 'vitest'

// Mock environment variables for unit tests
process.env.NODE_ENV = 'test'
process.env.DATABASE_URL = 'file:./test-unit.sqlite'
process.env.JWT_SECRET = 'test-jwt-secret-key'
process.env.API_BASE_URL = 'http://localhost:3000'

// Global mocks
global.fetch = vi.fn()

// Mock console methods to reduce noise in tests
const originalConsole = { ...console }
global.console = {
  ...console,
  log: vi.fn(),
  warn: vi.fn(),
  error: vi.fn(),
  info: vi.fn(),
  debug: vi.fn()
}

// Restore console after tests
afterAll(() => {
  global.console = originalConsole
})

// Mock localStorage for browser-like environment
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
  length: 0,
  key: vi.fn()
}

Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
  writable: true
})

// Mock sessionStorage
const sessionStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
  length: 0,
  key: vi.fn()
}

Object.defineProperty(window, 'sessionStorage', {
  value: sessionStorageMock,
  writable: true
})

// Mock IntersectionObserver
global.IntersectionObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn()
}))

// Mock ResizeObserver
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn()
}))

// Mock matchMedia
Object.defineProperty(window, 'matchMedia', {
  writable: true,
  value: vi.fn().mockImplementation(query => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn()
  }))
})

// Mock crypto for secure random values
Object.defineProperty(global, 'crypto', {
  value: {
    getRandomValues: vi.fn((arr) => {
      for (let i = 0; i < arr.length; i++) {
        arr[i] = Math.floor(Math.random() * 256)
      }
      return arr
    }),
    randomUUID: vi.fn(() => 'test-uuid-' + Math.random().toString(36).substr(2, 9))
  }
})

// Setup and teardown for each test
beforeEach(() => {
  // Clear all mocks before each test
  vi.clearAllMocks()
  
  // Reset localStorage and sessionStorage
  localStorageMock.clear()
  sessionStorageMock.clear()
  
  // Reset fetch mock
  vi.mocked(fetch).mockResolvedValue({
    ok: true,
    status: 200,
    json: () => Promise.resolve({}),
    text: () => Promise.resolve(''),
    headers: new Headers(),
    statusText: 'OK'
  } as Response)
})

afterEach(() => {
  // Clean up after each test
  vi.restoreAllMocks()
})

// Global test utilities
export const createMockResponse = (data: any, status = 200) => ({
  ok: status >= 200 && status < 300,
  status,
  json: () => Promise.resolve(data),
  text: () => Promise.resolve(JSON.stringify(data)),
  headers: new Headers(),
  statusText: status === 200 ? 'OK' : 'Error'
})

export const createMockError = (message: string, status = 500) => {
  const error = new Error(message)
  ;(error as any).status = status
  return error
}

// Mock data factories
export const createMockUser = (overrides = {}) => ({
  id: 'user-123',
  email: 'test@example.com',
  name: 'Test User',
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  ...overrides
})

export const createMockWeightEntry = (overrides = {}) => ({
  id: 'entry-123',
  userId: 'user-123',
  weight: 70.5,
  bodyFat: 15.0,
  date: new Date().toISOString(),
  notes: 'Test entry',
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  ...overrides
})

export const createMockGoal = (overrides = {}) => ({
  id: 'goal-123',
  userId: 'user-123',
  targetWeight: 65.0,
  targetBodyFat: 12.0,
  targetDate: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(),
  isActive: true,
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  ...overrides
})
