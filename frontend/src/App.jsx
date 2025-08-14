import React, { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import AdminPanel from './components/AdminPanel';
import { Button } from './components/ui/button';
import { MessageSquare, Settings, Building2 } from 'lucide-react';
import './App.css';

function App() {
  const [currentView, setCurrentView] = useState('chat');

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header de navegación */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <Building2 className="h-8 w-8 text-blue-600 mr-3" />
              <div>
                <h1 className="text-xl font-bold text-gray-900">HDL Distribuidora</h1>
                <p className="text-sm text-gray-500"></p>
              </div>
            </div>
            
            <nav className="flex space-x-4">
              <Button
                variant={currentView === 'chat' ? 'default' : 'outline'}
                onClick={() => setCurrentView('chat')}
                className="flex items-center"
              >
                <MessageSquare className="h-4 w-4 mr-2" />
                Chat
              </Button>
              <Button
                variant={currentView === 'admin' ? 'default' : 'outline'}
                onClick={() => setCurrentView('admin')}
                className="flex items-center"
              >
                <Settings className="h-4 w-4 mr-2" />
                Administración
              </Button>
            </nav>
          </div>
        </div>
      </header>

      {/* Contenido principal */}
      <main>
        {currentView === 'chat' ? (
          <ChatInterface />
        ) : (
          <AdminPanel />
        )}
      </main>
    </div>
  );
}

export default App;

