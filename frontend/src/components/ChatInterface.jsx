import { useState, useRef } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Textarea } from '@/components/ui/textarea'
import { 
  Send, 
  Paperclip, 
  Mic, 
  Image, 
  FileText, 
  Bot, 
  User,
  Upload,
  AlertCircle
} from 'lucide-react'
import apiService from '../services/api'

const ChatInterface = () => {
  const [messages, setMessages] = useState([])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [attachedFiles, setAttachedFiles] = useState([])
  const [error, setError] = useState(null)
  const fileInputRef = useRef(null)

  const handleSendMessage = async () => {
    if (!inputText.trim() && attachedFiles.length === 0) return

    const newMessage = {
      id: Date.now(),
      type: 'user',
      content: inputText,
      files: attachedFiles,
      timestamp: new Date()
    }

    setMessages(prev => [...prev, newMessage])
    setInputText('')
    setAttachedFiles([])
    setIsLoading(true)
    setError(null)

    try {
      // Procesar archivos
      const processedFiles = await apiService.processFiles(attachedFiles)
      
      // Preparar historial de conversación
      const history = messages.map(msg => ({
        role: msg.type === 'user' ? 'user' : 'assistant',
        content: msg.content
      }))

      // Enviar mensaje a la API
      const response = await apiService.sendMessage(inputText, history, processedFiles)
      
      const botResponse = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.response,
        quickReplies: response.quick_replies || [],
        products: response.products || [],
        clients: response.clients || [],
        nextStep: response.next_step,
        timestamp: new Date()
      }
      
      setMessages(prev => [...prev, botResponse])
      
    } catch (error) {
      console.error('Error sending message:', error)
      setError('Error al enviar el mensaje. Por favor, intenta nuevamente.')
      
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: 'Lo siento, hubo un error al procesar tu mensaje. Por favor, intenta nuevamente.',
        timestamp: new Date()
      }
      
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleFileUpload = (event) => {
    const files = Array.from(event.target.files)
    setAttachedFiles(prev => [...prev, ...files])
  }

  const removeFile = (index) => {
    setAttachedFiles(prev => prev.filter((_, i) => i !== index))
  }

  const handleQuickReply = (reply) => {
    setInputText(reply)
  }

  const handleProductSelect = async (product) => {
    const productMessage = `Me interesa el producto: ${product.nombre} (Código: ${product.codigo})`
    setInputText(productMessage)
  }

  const formatTime = (date) => {
    return date.toLocaleTimeString('es-AR', { 
      hour: '2-digit', 
      minute: '2-digit' 
    })
  }

  const formatPrice = (price) => {
    return new Intl.NumberFormat('es-AR', {
      style: 'currency',
      currency: 'ARS'
    }).format(parseFloat(price))
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b border-gray-200 p-4">
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center">
            <Bot className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-semibold text-gray-900">
              Ludmi AI
            </h1>
            <p className="text-sm text-gray-500">
              HDL Distribuidora
            </p>
          </div>
        </div>
      </div>

      {/* Error Banner */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-400 p-4">
          <div className="flex">
            <AlertCircle className="h-5 w-5 text-red-400" />
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
          </div>
        </div>
      )}

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className={`max-w-xs lg:max-w-md ${message.type === 'user' ? 'order-2' : 'order-1'}`}>
              <div
                className={`rounded-lg p-3 ${
                  message.type === 'user'
                    ? 'bg-blue-600 text-white'
                    : 'bg-white border border-gray-200'
                }`}
              >
                <p className="text-sm">{message.content}</p>
                
                {/* Files */}
                {message.files && message.files.length > 0 && (
                  <div className="mt-2 space-y-1">
                    {message.files.map((file, index) => (
                      <div key={index} className="flex items-center space-x-2 text-xs">
                        <FileText className="w-3 h-3" />
                        <span>{file.name}</span>
                      </div>
                    ))}
                  </div>
                )}

                {/* Products */}
                {message.products && message.products.length > 0 && (
                  <div className="mt-3 space-y-2">
                    <p className="text-xs text-gray-500">Productos encontrados:</p>
                    <div className="space-y-1 max-h-40 overflow-y-auto">
                      {message.products.slice(0, 5).map((product, index) => (
                        <Card key={index} className="p-2 cursor-pointer hover:bg-gray-50" 
                              onClick={() => handleProductSelect(product)}>
                          <div className="text-xs">
                            <p className="font-medium">{product.nombre}</p>
                            <p className="text-gray-500">Código: {product.codigo}</p>
                            {product.precios && product.precios.length > 0 && (
                              <p className="text-green-600 font-medium">
                                {formatPrice(product.precios[0].precio)}
                              </p>
                            )}
                          </div>
                        </Card>
                      ))}
                    </div>
                  </div>
                )}

                {/* Clients / Obras */}
                {message.clients && message.clients.length > 0 && (
                  <div className="mt-3 space-y-2">
                    <p className="text-xs text-gray-500">Clientes/Obras encontradas:</p>
                    <div className="space-y-2 max-h-48 overflow-y-auto">
                      {message.clients.slice(0, 10).map((client, cidx) => (
                        <Card key={cidx} className="p-2">
                          <div className="text-xs">
                            <p className="font-medium">{client.razon_social || 'Cliente'}</p>
                            {client.cuit && (
                              <p className="text-gray-500">CUIT: {client.cuit}</p>
                            )}
                            {client.obras && client.obras.length > 0 && (
                              <div className="mt-1 space-y-1">
                                {client.obras.map((obra, oidx) => (
                                  <div key={oidx} className="flex items-center justify-between bg-gray-50 border rounded p-1">
                                    <div>
                                      <p className="font-medium">{obra.nombre}</p>
                                      <p className="text-gray-500">Obra: {obra.codigo}</p>
                                    </div>
                                    <Button
                                      variant="outline"
                                      size="sm"
                                      onClick={() => handleQuickReply(`Usar obra ${obra.nombre} (codigo ${obra.codigo})`)}
                                      className="text-xs"
                                    >
                                      Usar
                                    </Button>
                                  </div>
                                ))}
                              </div>
                            )}
                          </div>
                        </Card>
                      ))}
                    </div>
                  </div>
                )}

                {/* Quick Replies */}
                {message.quickReplies && message.quickReplies.length > 0 && (
                  <div className="mt-3 space-y-2">
                    <p className="text-xs text-gray-500">Respuestas rápidas:</p>
                    <div className="flex flex-wrap gap-2">
                      {message.quickReplies.map((reply, index) => (
                        <Button
                          key={index}
                          variant="outline"
                          size="sm"
                          onClick={() => handleQuickReply(reply)}
                          className="text-xs"
                        >
                          {reply}
                        </Button>
                      ))}
                    </div>
                  </div>
                )}
              </div>
              
              <div className={`flex items-center mt-1 space-x-2 ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}>
                {message.type === 'user' ? (
                  <User className="w-4 h-4 text-gray-400" />
                ) : (
                  <Bot className="w-4 h-4 text-gray-400" />
                )}
                <span className="text-xs text-gray-500">
                  {formatTime(message.timestamp)}
                </span>
              </div>
            </div>
          </div>
        ))}

        {/* Loading indicator */}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 rounded-lg p-3">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Input Area */}
      <div className="bg-white border-t border-gray-200 p-4">
        {/* Attached Files */}
        {attachedFiles.length > 0 && (
          <div className="mb-3 flex flex-wrap gap-2">
            {attachedFiles.map((file, index) => (
              <Badge key={index} variant="secondary" className="flex items-center space-x-1">
                <FileText className="w-3 h-3" />
                <span className="text-xs">{file.name}</span>
                <button
                  onClick={() => removeFile(index)}
                  className="ml-1 text-gray-500 hover:text-gray-700"
                >
                  ×
                </button>
              </Badge>
            ))}
          </div>
        )}

        <div className="flex space-x-2">
          <div className="flex-1">
            <Textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Escribe tu mensaje aquí..."
              className="min-h-[40px] max-h-32 resize-none"
              onKeyPress={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault()
                  handleSendMessage()
                }
              }}
            />
          </div>
          
          <div className="flex flex-col space-y-2">
            <input
              type="file"
              ref={fileInputRef}
              onChange={handleFileUpload}
              multiple
              accept=".pdf,.jpg,.jpeg,.png,.mp3,.wav,.m4a"
              className="hidden"
            />
            
            <Button
              variant="outline"
              size="sm"
              onClick={() => fileInputRef.current?.click()}
              className="p-2"
              disabled={isLoading}
            >
              <Paperclip className="w-4 h-4" />
            </Button>
            
            <Button
              onClick={handleSendMessage}
              disabled={(!inputText.trim() && attachedFiles.length === 0) || isLoading}
              className="p-2"
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
        </div>

        <div className="mt-2 flex justify-center space-x-4 text-xs text-gray-500">
          <span className="flex items-center space-x-1">
            <Image className="w-3 h-3" />
            <span>Imágenes</span>
          </span>
          <span className="flex items-center space-x-1">
            <FileText className="w-3 h-3" />
            <span>PDFs</span>
          </span>
          <span className="flex items-center space-x-1">
            <Mic className="w-3 h-3" />
            <span>Audio</span>
          </span>
        </div>
      </div>
    </div>
  )
}

export default ChatInterface

