import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from './ui/card';
import { Button } from './ui/button';
import { Input } from './ui/input';
import { Textarea } from './ui/textarea';
import { Tabs, TabsContent, TabsList, TabsTrigger } from './ui/tabs';
import { Badge } from './ui/badge';
import { 
  FileText, 
  Download, 
  Search, 
  Plus, 
  Trash2, 
  Edit,
  Calendar,
  DollarSign,
  Package,
  Users
} from 'lucide-react';

const AdminPanel = () => {
  const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api';
  const [budgets, setBudgets] = useState([]);
  const [knowledge, setKnowledge] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');
  const [newKnowledge, setNewKnowledge] = useState({
    title: '',
    content: '',
    category: 'empresa'
  });

  // Cargar presupuestos
  const loadBudgets = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/budget/list`);
      const data = await response.json();
      setBudgets(data.budgets || []);
    } catch (error) {
      console.error('Error al cargar presupuestos:', error);
    } finally {
      setLoading(false);
    }
  };

  // Cargar conocimiento
  const loadKnowledge = async () => {
    try {
      const response = await fetch(`${API_BASE}/knowledge/list`);
      const data = await response.json();
      setKnowledge(data.knowledge || []);
    } catch (error) {
      console.error('Error al cargar conocimiento:', error);
      setKnowledge([]);
    }
  };

  // Agregar nuevo conocimiento
  const addKnowledge = async () => {
    if (!newKnowledge.title || !newKnowledge.content) return;

    try {
      const response = await fetch(`${API_BASE}/knowledge/add`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newKnowledge),
      });

      if (response.ok) {
        setNewKnowledge({ title: '', content: '', category: 'empresa' });
        loadKnowledge();
      }
    } catch (error) {
      console.error('Error al agregar conocimiento:', error);
    }
  };

  // Descargar PDF de presupuesto
  const downloadBudgetPDF = async (budgetId) => {
    try {
      const response = await fetch(`${API_BASE}/budget/${budgetId}`);
      const data = await response.json();
      
      const pdfResponse = await fetch(`${API_BASE}/budget/generate-pdf`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ budget: data.budget }),
      });

      if (pdfResponse.ok) {
        const blob = await pdfResponse.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `presupuesto_${budgetId}.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      }
    } catch (error) {
      console.error('Error al descargar PDF:', error);
    }
  };

  useEffect(() => {
    loadBudgets();
    loadKnowledge();
  }, []);

  // Filtrar presupuestos
  const filteredBudgets = budgets.filter(budget =>
    budget.client_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    budget.id?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Filtrar conocimiento
  const filteredKnowledge = knowledge.filter(item =>
    item.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    item.content?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Estadísticas
  const totalBudgets = budgets.length;
  const totalAmount = budgets.reduce((sum, budget) => sum + (budget.total || 0), 0);
  const avgAmount = totalBudgets > 0 ? totalAmount / totalBudgets : 0;

  return (
    <div className="min-h-screen bg-gray-50 p-6">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">Panel de Administración</h1>
          <p className="text-gray-600">Gestiona presupuestos y conocimiento de la empresa</p>
        </div>

        {/* Estadísticas */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <FileText className="h-8 w-8 text-blue-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Total Presupuestos</p>
                  <p className="text-2xl font-bold text-gray-900">{totalBudgets}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <DollarSign className="h-8 w-8 text-green-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Monto Total</p>
                  <p className="text-2xl font-bold text-gray-900">${totalAmount.toLocaleString()}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <Package className="h-8 w-8 text-purple-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Promedio</p>
                  <p className="text-2xl font-bold text-gray-900">${avgAmount.toLocaleString()}</p>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <div className="flex items-center">
                <Users className="h-8 w-8 text-orange-600" />
                <div className="ml-4">
                  <p className="text-sm font-medium text-gray-600">Base Conocimiento</p>
                  <p className="text-2xl font-bold text-gray-900">{knowledge.length}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Barra de búsqueda */}
        <div className="mb-6">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <Input
              placeholder="Buscar presupuestos, clientes o conocimiento..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>

        {/* Tabs principales */}
        <Tabs defaultValue="budgets" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="budgets">Presupuestos</TabsTrigger>
            <TabsTrigger value="knowledge">Base de Conocimiento</TabsTrigger>
          </TabsList>

          {/* Tab de Presupuestos */}
          <TabsContent value="budgets" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>Historial de Presupuestos</CardTitle>
                <CardDescription>
                  Lista de todos los presupuestos generados
                </CardDescription>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="text-center py-8">
                    <p className="text-gray-500">Cargando presupuestos...</p>
                  </div>
                ) : filteredBudgets.length === 0 ? (
                  <div className="text-center py-8">
                    <FileText className="mx-auto h-12 w-12 text-gray-400" />
                    <p className="mt-2 text-gray-500">No hay presupuestos disponibles</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {filteredBudgets.map((budget) => (
                      <div key={budget.id} className="border rounded-lg p-4 hover:bg-gray-50">
                        <div className="flex items-center justify-between">
                          <div className="flex-1">
                            <div className="flex items-center space-x-2">
                              <h3 className="font-semibold text-gray-900">{budget.id}</h3>
                              <Badge variant="outline">{budget.items_count} items</Badge>
                            </div>
                            <p className="text-sm text-gray-600 mt-1">
                              Cliente: {budget.client_name || 'Sin nombre'}
                            </p>
                            <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                              <span className="flex items-center">
                                <Calendar className="h-4 w-4 mr-1" />
                                {new Date(budget.created_at).toLocaleDateString()}
                              </span>
                              <span className="flex items-center">
                                <DollarSign className="h-4 w-4 mr-1" />
                                ${budget.total?.toLocaleString()}
                              </span>
                            </div>
                          </div>
                          <div className="flex space-x-2">
                            <Button
                              variant="outline"
                              size="sm"
                              onClick={() => downloadBudgetPDF(budget.id)}
                            >
                              <Download className="h-4 w-4 mr-1" />
                              PDF
                            </Button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>

          {/* Tab de Base de Conocimiento */}
          <TabsContent value="knowledge" className="space-y-4">
            {/* Formulario para agregar conocimiento */}
            <Card>
              <CardHeader>
                <CardTitle>Agregar Conocimiento</CardTitle>
                <CardDescription>
                  Agrega información sobre la empresa, productos o políticas
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <Input
                    placeholder="Título del conocimiento"
                    value={newKnowledge.title}
                    onChange={(e) => setNewKnowledge({...newKnowledge, title: e.target.value})}
                  />
                  <select
                    className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    value={newKnowledge.category}
                    onChange={(e) => setNewKnowledge({...newKnowledge, category: e.target.value})}
                  >
                    <option value="empresa">Información de Empresa</option>
                    <option value="productos">Productos y Materiales</option>
                    <option value="politicas">Políticas y Procedimientos</option>
                    <option value="precios">Precios y Descuentos</option>
                    <option value="otros">Otros</option>
                  </select>
                </div>
                <Textarea
                  placeholder="Contenido del conocimiento..."
                  value={newKnowledge.content}
                  onChange={(e) => setNewKnowledge({...newKnowledge, content: e.target.value})}
                  rows={4}
                />
                <Button onClick={addKnowledge} className="w-full">
                  <Plus className="h-4 w-4 mr-2" />
                  Agregar Conocimiento
                </Button>
              </CardContent>
            </Card>

            {/* Lista de conocimiento */}
            <Card>
              <CardHeader>
                <CardTitle>Base de Conocimiento</CardTitle>
                <CardDescription>
                  Información disponible para el asistente de IA
                </CardDescription>
              </CardHeader>
              <CardContent>
                {filteredKnowledge.length === 0 ? (
                  <div className="text-center py-8">
                    <Package className="mx-auto h-12 w-12 text-gray-400" />
                    <p className="mt-2 text-gray-500">No hay conocimiento disponible</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {filteredKnowledge.map((item) => (
                      <div key={item.id} className="border rounded-lg p-4 hover:bg-gray-50">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center space-x-2">
                              <h3 className="font-semibold text-gray-900">{item.title}</h3>
                              <Badge variant="secondary">{item.category}</Badge>
                            </div>
                            <p className="text-sm text-gray-600 mt-2 line-clamp-3">
                              {item.content}
                            </p>
                            <p className="text-xs text-gray-400 mt-2">
                              Creado: {new Date(item.created_at).toLocaleDateString()}
                            </p>
                          </div>
                          <div className="flex space-x-2 ml-4">
                            <Button variant="outline" size="sm">
                              <Edit className="h-4 w-4" />
                            </Button>
                            <Button variant="outline" size="sm">
                              <Trash2 className="h-4 w-4" />
                            </Button>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
};

export default AdminPanel;

