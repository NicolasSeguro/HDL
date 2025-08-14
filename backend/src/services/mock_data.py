"""
Datos de prueba para desarrollo cuando las APIs externas no están disponibles
"""

MOCK_SOCIEDADES = {
    "resultado": 1,
    "sociedades": [
        {
            "nombre": "DLM Construccion SRL",
            "codigo": "15",
            "sucursales": [
                {
                    "nombre": "DLM",
                    "codigo": "17"
                }
            ]
        },
        {
            "nombre": "HDL Distribuidora SRL",
            "codigo": "16",
            "sucursales": [
                {
                    "nombre": "HDL Central",
                    "codigo": "18"
                }
            ]
        },
        {
            "nombre": "Materiales y Logistica SRL",
            "codigo": "17",
            "sucursales": [
                {
                    "nombre": "MyL",
                    "codigo": "20"
                }
            ]
        },
        {
            "nombre": "HDL URBANA S.R.L.",
            "codigo": "22",
            "sucursales": [
                {
                    "nombre": "HDL URBANA",
                    "codigo": "29"
                }
            ]
        }
    ]
}

MOCK_CLIENTES_OBRAS = {
    "resultado": 1,
    "clientes": [
        {
            "datos": {
                "email": "cliente@ejemplo.com",
                "cuit": "20316528210",
                "telefono": "20316528210",
                "razon_social": "Cliente Ejemplo SA"
            },
            "sociedades": [
                {
                    "codigo": "16",
                    "nombre": "HDL Distribuidora SRL"
                },
                {
                    "codigo": "17",
                    "nombre": "Materiales y Logistica SRL"
                }
            ],
            "obras": [
                {
                    "codigo": "155",
                    "nombre": "Casa Particular 120m2",
                    "listas": [
                        {
                            "nombre": "14462",
                            "codigo": "Lista Obra C12"
                        },
                        {
                            "nombre": "13186",
                            "codigo": "Lista Obra C20"
                        }
                    ]
                },
                {
                    "codigo": "135",
                    "nombre": "Edificio Residencial",
                    "listas": [
                        {
                            "nombre": "14462",
                            "codigo": "Lista Obra C12"
                        }
                    ]
                }
            ]
        }
    ]
}

MOCK_ARTICULOS = {
    "resultado": 1,
    "articulos": [
        {
            "codigo": "10104",
            "nombre": "PIEDRA PARTIDA (6a20) X M3 CAMION",
            "codigoint": "230011",
            "precios": [
                {
                    "codigo": "14462",
                    "nombre": "Lista Obra C12",
                    "precio": "79794.368"
                },
                {
                    "codigo": "13186",
                    "nombre": "Lista Obra C20",
                    "precio": "75000.000"
                }
            ]
        },
        {
            "codigo": "10120",
            "nombre": "PIEDRA PARTIDA (6a20) X M3",
            "codigoint": "230010",
            "precios": [
                {
                    "codigo": "14462",
                    "nombre": "Lista Obra C12",
                    "precio": "71066.667"
                }
            ]
        },
        {
            "codigo": "30101",
            "nombre": "LADRILLO COMUN",
            "codigoint": "300001",
            "precios": [
                {
                    "codigo": "14462",
                    "nombre": "Lista Obra C12",
                    "precio": "192.391"
                }
            ]
        },
        {
            "codigo": "30104",
            "nombre": "LADRILLO HUECO 8X18X33",
            "codigoint": "300004",
            "precios": [
                {
                    "codigo": "14462",
                    "nombre": "Lista Obra C12",
                    "precio": "579.870"
                }
            ]
        },
        {
            "codigo": "50103",
            "nombre": "CEMENTO AVELLANEDA X 50 KG",
            "codigoint": "500003",
            "precios": [
                {
                    "codigo": "14462",
                    "nombre": "Lista Obra C12",
                    "precio": "8500.000"
                }
            ]
        },
        {
            "codigo": "50108",
            "nombre": "CAL MILAGRO X 25 KG",
            "codigoint": "500008",
            "precios": [
                {
                    "codigo": "14462",
                    "nombre": "Lista Obra C12",
                    "precio": "4500.000"
                }
            ]
        },
        {
            "codigo": "50115",
            "nombre": "YESO ALPRESS x 35 KG",
            "codigoint": "500015",
            "precios": [
                {
                    "codigo": "14462",
                    "nombre": "Lista Obra C12",
                    "precio": "6200.000"
                }
            ]
        },
        {
            "codigo": "60001",
            "nombre": "KLAUKOL IMPERMEABLE POTENCIADO X 30 KG",
            "codigoint": "600001",
            "precios": [
                {
                    "codigo": "14462",
                    "nombre": "Lista Obra C12",
                    "precio": "12500.000"
                }
            ]
        },
        {
            "codigo": "70001",
            "nombre": "BLOQUE RETAK BQ 12.5X25X50",
            "codigoint": "700001",
            "precios": [
                {
                    "codigo": "14462",
                    "nombre": "Lista Obra C12",
                    "precio": "850.000"
                }
            ]
        },
        {
            "codigo": "10118",
            "nombre": "ARENA X M3 CAMION",
            "codigoint": "230018",
            "precios": [
                {
                    "codigo": "14462",
                    "nombre": "Lista Obra C12",
                    "precio": "37696.117"
                }
            ]
        }
    ]
}

