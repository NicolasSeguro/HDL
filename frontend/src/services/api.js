const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api'

class ApiService {
  constructor() {
    this.baseURL = API_BASE_URL
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    }

    try {
      const response = await fetch(url, config)
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`)
      }
      
      return await response.json()
    } catch (error) {
      console.error('API request failed:', error)
      throw error
    }
  }

  // Chat endpoints
  async sendMessage(message, history = [], files = []) {
    return this.request('/chat/message', {
      method: 'POST',
      body: JSON.stringify({
        message,
        history,
        files,
        timestamp: Date.now()
      })
    })
  }

  async searchProducts(query, limit = 50) {
    return this.request('/chat/search-products', {
      method: 'POST',
      body: JSON.stringify({
        query,
        limit
      })
    })
  }

  async getProduct(codigo) {
    return this.request(`/chat/product/${codigo}`)
  }

  async getSocieties() {
    return this.request('/chat/societies')
  }

  async getPriceLists(codigoObra) {
    return this.request(`/chat/price-lists/${codigoObra}`)
  }

  async analyzeImage(imageData) {
    return this.request('/chat/analyze-image', {
      method: 'POST',
      body: JSON.stringify({
        image_data: imageData
      })
    })
  }

  async generateBudget(items, clientInfo = {}) {
    return this.request('/chat/generate-budget', {
      method: 'POST',
      body: JSON.stringify({
        items,
        client_info: clientInfo
      })
    })
  }

  async clearCache() {
    return this.request('/chat/clear-cache', {
      method: 'POST'
    })
  }

  // Utility methods
  fileToBase64(file) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.readAsDataURL(file)
      reader.onload = () => {
        const base64 = reader.result.split(',')[1]
        resolve(base64)
      }
      reader.onerror = error => reject(error)
    })
  }

  async processFiles(files) {
    const processedFiles = []
    
    for (const file of files) {
      try {
        if (file.type.startsWith('image/')) {
          const base64 = await this.fileToBase64(file)
          processedFiles.push({
            type: 'image',
            name: file.name,
            data: base64
          })
        } else if (file.type.startsWith('audio/')) {
          const base64 = await this.fileToBase64(file)
          processedFiles.push({
            type: 'audio',
            name: file.name,
            data: base64
          })
        } else {
          console.warn(`Unsupported file type: ${file.type}`)
        }
      } catch (error) {
        console.error(`Error processing file ${file.name}:`, error)
      }
    }
    
    return processedFiles
  }
}

export default new ApiService()

