import { ref, watch } from 'vue'

const isDarkMode = ref(false)

// Initialize from localStorage
if (typeof window !== 'undefined') {
  const saved = localStorage.getItem('darkMode')
  if (saved !== null) {
    isDarkMode.value = saved === 'true'
  }
}

// Apply dark mode to document
const applyDarkMode = (dark) => {
  if (typeof document !== 'undefined') {
    if (dark) {
      document.documentElement.setAttribute('data-theme', 'dark')
    } else {
      document.documentElement.setAttribute('data-theme', 'light')
    }
  }
}

// Watch for changes and apply
watch(isDarkMode, (newValue) => {
  applyDarkMode(newValue)
  if (typeof window !== 'undefined') {
    localStorage.setItem('darkMode', newValue.toString())
  }
}, { immediate: true })

// Apply immediately on module load
if (typeof window !== 'undefined') {
  applyDarkMode(isDarkMode.value)
}

export function useDarkMode() {
  const toggleDarkMode = () => {
    isDarkMode.value = !isDarkMode.value
  }

  return {
    isDarkMode,
    toggleDarkMode
  }
}

