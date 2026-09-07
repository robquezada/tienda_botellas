import React, { useDeferredValue, useEffect, useState, startTransition } from 'react'
import { createRoot } from 'react-dom/client'
import './styles.css'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000/api'
const ORDER_STATUS_OPTIONS = ['Cancelado', 'Surtido', 'Pagado','pendiente']
const PAGE_BY_HASH = {
  '#pedidos': 'pedidos',
  '#clientes': 'clientes',
}

const fallbackProducts = [
  {
    id: 'demo-1',
    name: 'Botella Ambar Premium',
    description: 'Vidrio ambar para bebidas artesanales, aceites y kombucha.',
    material: 'vidrio',
    capacity_ml: 500,
    price: 2.75,
    stock: 180,
    image_url: 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?auto=format&fit=crop&w=900&q=80',
  },
  {
    id: 'demo-2',
    name: 'PET Cristal Eco',
    description: 'Plastico ligero, reciclable y resistente para agua y jugos.',
    material: 'plastico',
    capacity_ml: 1000,
    price: 0.85,
    stock: 900,
    image_url: 'https://images.unsplash.com/photo-1605405363458-2d028ed8a588?auto=format&fit=crop&w=900&q=80',
  },
  {
    id: 'demo-3',
    name: 'Vidrio Swing Top',
    description: 'Cierre hermetico reutilizable para marcas gourmet.',
    material: 'vidrio',
    capacity_ml: 750,
    price: 4.9,
    stock: 95,
    image_url: 'https://images.unsplash.com/photo-1523362628745-0c100150b504?auto=format&fit=crop&w=900&q=80',
  },
]

function App() {
  const [currentPage, setCurrentPage] = useState(() => PAGE_BY_HASH[window.location.hash] ?? 'productos')
  const [products, setProducts] = useState([])
  const [orders, setOrders] = useState([])
  const [clients, setClients] = useState([])
  const [cart, setCart] = useState([])
  const [customer, setCustomer] = useState({ name: '', email: '', phone: '', address: '' })
  const [loading, setLoading] = useState(true)
  const [ordersLoading, setOrdersLoading] = useState(true)
  const [clientsLoading, setClientsLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [savingStatus, setSavingStatus] = useState(false)
  const [apiStatus, setApiStatus] = useState('Conectando con API')
  const [orderMessage, setOrderMessage] = useState('')
  const [statusMessage, setStatusMessage] = useState('')
  const [editingOrderId, setEditingOrderId] = useState('')
  const [statusDraft, setStatusDraft] = useState('Pagado')
  const [orderSearch, setOrderSearch] = useState('')
  const [clientSearch, setClientSearch] = useState('')
  const [orderPage, setOrderPage] = useState(1)
  const [clientPage, setClientPage] = useState(1)
  const [orderSort, setOrderSort] = useState({ field: 'created_at', direction: 'desc' })
  const [clientSort, setClientSort] = useState({ field: 'created_at', direction: 'desc' })
  const deferredOrderSearch = useDeferredValue(orderSearch)
  const deferredClientSearch = useDeferredValue(clientSearch)
  const pageSize = 5

  useEffect(() => {
    fetch(`${API_URL}/products`)
      .then((response) => {
        if (!response.ok) throw new Error('API no disponible')
        return response.json()
      })
      .then((data) => {
        startTransition(() => {
          setProducts(data.length ? data : fallbackProducts)
          setApiStatus(data.length ? 'Catalogo en vivo' : 'API conectada, sin productos')
        })
      })
      .catch(() => {
        setProducts(fallbackProducts)
        setApiStatus('Modo demo: inicia FastAPI para datos reales')
      })
      .finally(() => setLoading(false))
  }, [])

  const loadOrders = async () => {
    setOrdersLoading(true)
    try {
      const response = await fetch(`${API_URL}/orders`)
      if (!response.ok) throw new Error('No se pudieron cargar los pedidos')
      const data = await response.json()
      setOrders(data)
    } catch {
      setOrders([])
    } finally {
      setOrdersLoading(false)
    }
  }

  const loadClients = async () => {
    setClientsLoading(true)
    try {
      const response = await fetch(`${API_URL}/clients`)
      if (!response.ok) throw new Error('No se pudieron cargar los clientes')
      const data = await response.json()
      setClients(data)
    } catch {
      setClients([])
    } finally {
      setClientsLoading(false)
    }
  }

  useEffect(() => {
    loadOrders()
    loadClients()
  }, [])

  useEffect(() => {
    const updatePage = () => setCurrentPage(PAGE_BY_HASH[window.location.hash] ?? 'productos')
    window.addEventListener('hashchange', updatePage)
    return () => window.removeEventListener('hashchange', updatePage)
  }, [])

  const addToCart = (product) => {
    setCart((current) => {
      const existing = current.find((item) => item.id === product.id)
      if (existing) {
        return current.map((item) => (item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item))
      }
      return [...current, { ...product, quantity: 1 }]
    })
  }

  const updateCustomer = (event) => {
    const { name, value } = event.target
    setCustomer((current) => ({ ...current, [name]: value }))
  }

  const saveOrder = async (event) => {
    event.preventDefault()
    setOrderMessage('')

    if (cart.length === 0) {
      setOrderMessage('Agrega al menos un producto al pedido.')
      return
    }

    if (cart.some((item) => item.id.startsWith('demo-'))) {
      setOrderMessage('Inicia la API y usa productos reales para guardar la orden.')
      return
    }

    setSaving(true)
    try {
      const customerResponse = await fetch(`${API_URL}/customers`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(customer),
      })

      if (!customerResponse.ok) {
        const error = await customerResponse.json()
        throw new Error(error.detail ?? 'No se pudo crear el cliente')
      }

      const savedCustomer = await customerResponse.json()
      const orderResponse = await fetch(`${API_URL}/orders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          customer_id: savedCustomer.id,
          items: cart.map((item) => ({ product_id: item.id, quantity: item.quantity })),
        }),
      })

      if (!orderResponse.ok) {
        const error = await orderResponse.json()
        throw new Error(error.detail ?? 'No se pudo guardar la orden')
      }

      const savedOrder = await orderResponse.json()
      setCart([])
      setOrderMessage(`Orden guardada: ${savedOrder.id}`)
      await loadOrders()
      await loadClients()
    } catch (error) {
      setOrderMessage(error.message)
    } finally {
      setSaving(false)
    }
  }

  const total = cart.reduce((sum, item) => sum + item.price * item.quantity, 0)
  const getCustomerName = (customerId) => clients.find((client) => client.id === customerId)?.name ?? 'Cliente no disponible'
  const normalizedSearch = deferredOrderSearch.trim().toLowerCase()
  const filteredOrders = orders.filter((order) => {
    const searchable = [
      order.id,
      getCustomerName(order.customer_id),
      order.status,
      order.total,
      order.created_at,
      order.items.map((item) => item.product_name).join(' '),
    ].join(' ').toLowerCase()
    return searchable.includes(normalizedSearch)
  })
  const sortedOrders = [...filteredOrders].sort((a, b) => {
    const getValue = (order) => {
      if (orderSort.field === 'items') return order.items.map((item) => item.product_name).join(', ')
      if (orderSort.field === 'quantity') return order.items.reduce((sum, item) => sum + item.quantity, 0)
      if (orderSort.field === 'customer_id') return getCustomerName(order.customer_id)
      return order[orderSort.field]
    }
    const aValue = getValue(a)
    const bValue = getValue(b)
    const comparison = typeof aValue === 'number' && typeof bValue === 'number'
      ? aValue - bValue
      : String(aValue).localeCompare(String(bValue))
    return orderSort.direction === 'asc' ? comparison : comparison * -1
  })
  const totalOrderPages = Math.max(1, Math.ceil(sortedOrders.length / pageSize))
  const currentOrderPage = Math.min(orderPage, totalOrderPages)
  const paginatedOrders = sortedOrders.slice((currentOrderPage - 1) * pageSize, currentOrderPage * pageSize)
  const normalizedClientSearch = deferredClientSearch.trim().toLowerCase()
  const filteredClients = clients.filter((client) => {
    const searchable = [client.id, client.name, client.email, client.phone, client.address, client.created_at].join(' ').toLowerCase()
    return searchable.includes(normalizedClientSearch)
  })
  const sortedClients = [...filteredClients].sort((a, b) => {
    const aValue = a[clientSort.field]
    const bValue = b[clientSort.field]
    const comparison = String(aValue).localeCompare(String(bValue))
    return clientSort.direction === 'asc' ? comparison : comparison * -1
  })
  const totalClientPages = Math.max(1, Math.ceil(sortedClients.length / pageSize))
  const currentClientPage = Math.min(clientPage, totalClientPages)
  const paginatedClients = sortedClients.slice((currentClientPage - 1) * pageSize, currentClientPage * pageSize)

  const changeOrderSort = (field) => {
    setOrderSort((current) => ({
      field,
      direction: current.field === field && current.direction === 'asc' ? 'desc' : 'asc',
    }))
    setOrderPage(1)
  }

  const changeClientSort = (field) => {
    setClientSort((current) => ({
      field,
      direction: current.field === field && current.direction === 'asc' ? 'desc' : 'asc',
    }))
    setClientPage(1)
  }

  const updateOrderSearch = (event) => {
    setOrderSearch(event.target.value)
    setOrderPage(1)
  }

  const updateClientSearch = (event) => {
    setClientSearch(event.target.value)
    setClientPage(1)
  }

  const startStatusEdit = (order) => {
    setStatusMessage('')
    setEditingOrderId(order.id)
    setStatusDraft(ORDER_STATUS_OPTIONS.includes(order.status) ? order.status : 'Pagado')
  }

  const saveOrderStatus = async (orderId) => {
    setSavingStatus(true)
    setStatusMessage('')
    try {
      const response = await fetch(`${API_URL}/orders/${orderId}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ status: statusDraft }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail ?? 'No se pudo modificar el estado')
      }

      await loadOrders()
      setEditingOrderId('')
      setStatusMessage('Estado actualizado correctamente.')
    } catch (error) {
      setStatusMessage(error.message)
    } finally {
      setSavingStatus(false)
    }
  }

  return (
    <main>
      <header className="site-header">
        <nav aria-label="Navegacion principal">
          <a className="brand" href="#productos">Bottega</a>
          <a className={currentPage === 'productos' ? 'active' : ''} href="#productos" aria-current={currentPage === 'productos' ? 'page' : undefined}>Ver Productos</a>
          <a className={currentPage === 'pedidos' ? 'active' : ''} href="#pedidos" aria-current={currentPage === 'pedidos' ? 'page' : undefined}>Ver Pedidos</a>
          <a className={currentPage === 'clientes' ? 'active' : ''} href="#clientes" aria-current={currentPage === 'clientes' ? 'page' : undefined}>Ver Clientes</a>
          <span>{apiStatus}</span>
        </nav>
      </header>

      {currentPage === 'productos' ? <>
      <section className="hero">
        <div className="hero-grid">
          <div className="hero-copy">
            <p className="eyebrow">Vidrio y plastico para marcas que embotellan mejor</p>
            <h1>Botellas listas para tu siguiente lote.</h1>
            <p>
              Compra botellas premium por unidad o volumen. Catalogo moderno, stock visible y API lista para operaciones.
            </p>
            <div className="hero-actions">
              <a className="primary" href="#catalogo">Ver productos</a>
              <a className="secondary" href="#pedidos">Ver pedidos</a>
              <a className="secondary" href="#clientes">Ver clientes</a>
              <a className="secondary" href="http://localhost:8000/docs">Docs API</a>
            </div>
          </div>
          <div className="showcase-card">
            <div className="bottle-shape"></div>
            <div>
              <span>Top venta</span>
              <h2>Vidrio Ambar 500ml</h2>
              <p>Proteccion UV, acabado premium y empaque seguro.</p>
            </div>
          </div>
        </div>
      </section>

      <section className="metrics">
        <article><strong>2</strong><span>materiales</span></article>
        <article><strong>24h</strong><span>preparacion</span></article>
        <article><strong>+1k</strong><span>unidades listas</span></article>
      </section>

      <section id="catalogo" className="catalog">
        <div className="section-heading">
          <p>Catalogo</p>
          <h2>Elige formato, material y capacidad.</h2>
        </div>

        {loading ? <p className="loading">Cargando productos...</p> : null}
        <div className="product-grid">
          {products.map((product) => (
            <article className="product-card" key={product.id}>
              <img src={product.image_url} alt={product.name} />
              <div className="product-content">
                <div className="pill-row">
                  <span>{product.material}</span>
                  <span>{product.capacity_ml} ml</span>
                </div>
                <h3>{product.name}</h3>
                <p>{product.description}</p>
                <div className="buy-row">
                  <strong>${product.price.toFixed(2)}</strong>
                  <button onClick={() => addToCart(product)}>Agregar</button>
                </div>
                <small>{product.stock} unidades disponibles</small>
              </div>
            </article>
          ))}
        </div>
      </section>
      </> : null}

      {currentPage === 'pedidos' ? <>
      <section id="lista-pedidos" className="orders-section">
        <div className="section-heading orders-heading">
          <div>
            <p>Pedidos</p>
            <h2>Ordenes guardadas en MongoDB.</h2>
          </div>
          <label className="search-box">
            Buscar pedido
            <input value={orderSearch} onChange={updateOrderSearch} placeholder="ID, cliente, estado, producto..." />
          </label>
        </div>

        <div className="orders-table-card">
          {ordersLoading ? <p className="loading">Cargando pedidos...</p> : null}
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th><button type="button" onClick={() => changeOrderSort('id')}>ID</button></th>
                  <th><button type="button" onClick={() => changeOrderSort('customer_id')}>Cliente</button></th>
                  <th><button type="button" onClick={() => changeOrderSort('items')}>Productos</button></th>
                  <th><button type="button" onClick={() => changeOrderSort('quantity')}>Cantidad</button></th>
                  <th><button type="button" onClick={() => changeOrderSort('status')}>Estado</button></th>
                  <th><button type="button" onClick={() => changeOrderSort('total')}>Total</button></th>
                  <th><button type="button" onClick={() => changeOrderSort('created_at')}>Fecha</button></th>
                  <th>Modificar</th>
                </tr>
              </thead>
              <tbody>
                {paginatedOrders.map((order) => (
                  <tr key={order.id}>
                    <td>{order.id.slice(-8)}</td>
                    <td>{getCustomerName(order.customer_id)}</td>
                    <td>{order.items.map((item) => item.product_name).join(', ')}</td>
                    <td>{order.items.reduce((sum, item) => sum + item.quantity, 0)}</td>
                    <td><span className="status-pill">{order.status}</span></td>
                    <td>${order.total.toFixed(2)}</td>
                    <td>{new Date(order.created_at).toLocaleDateString('es-DO')}</td>
                    <td>
                      {editingOrderId === order.id ? (
                        <div className="status-edit">
                          <select value={statusDraft} onChange={(event) => setStatusDraft(event.target.value)}>
                            {ORDER_STATUS_OPTIONS.map((status) => <option key={status} value={status}>{status}</option>)}
                          </select>
                          <button type="button" onClick={() => saveOrderStatus(order.id)} disabled={savingStatus}>Guardar</button>
                          <button className="ghost-button" type="button" onClick={() => setEditingOrderId('')} disabled={savingStatus}>Cancelar</button>
                        </div>
                      ) : (
                        <button className="table-action" type="button" onClick={() => startStatusEdit(order)}>Modificar</button>
                      )}
                    </td>
                  </tr>
                ))}
                {!ordersLoading && paginatedOrders.length === 0 ? (
                  <tr>
                    <td colSpan="8" className="empty-row">No hay pedidos para mostrar.</td>
                  </tr>
                ) : null}
              </tbody>
            </table>
          </div>

          {statusMessage ? <p className="table-message">{statusMessage}</p> : null}

          <div className="pagination">
            <span>{sortedOrders.length} pedidos encontrados</span>
            <div>
              <button type="button" onClick={() => setOrderPage((page) => Math.max(1, page - 1))} disabled={currentOrderPage === 1}>Anterior</button>
              <strong>{currentOrderPage} / {totalOrderPages}</strong>
              <button type="button" onClick={() => setOrderPage((page) => Math.min(totalOrderPages, page + 1))} disabled={currentOrderPage === totalOrderPages}>Siguiente</button>
            </div>
          </div>
        </div>
      </section>
      </> : null}

      {currentPage === 'clientes' ? <>
      <section id="lista-clientes" className="orders-section clients-section">
        <div className="section-heading orders-heading">
          <div>
            <p>Clientes</p>
            <h2>Clientes guardados en MongoDB.</h2>
          </div>
          <label className="search-box">
            Buscar cliente
            <input value={clientSearch} onChange={updateClientSearch} placeholder="ID, nombre, email, telefono..." />
          </label>
        </div>

        <div className="orders-table-card">
          {clientsLoading ? <p className="loading">Cargando clientes...</p> : null}
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th><button type="button" onClick={() => changeClientSort('id')}>ID</button></th>
                  <th><button type="button" onClick={() => changeClientSort('name')}>Nombre</button></th>
                  <th><button type="button" onClick={() => changeClientSort('email')}>Email</button></th>
                  <th><button type="button" onClick={() => changeClientSort('phone')}>Telefono</button></th>
                  <th><button type="button" onClick={() => changeClientSort('address')}>Direccion</button></th>
                  <th><button type="button" onClick={() => changeClientSort('created_at')}>Fecha</button></th>
                </tr>
              </thead>
              <tbody>
                {paginatedClients.map((client) => (
                  <tr key={client.id}>
                    <td>{client.id.slice(-8)}</td>
                    <td>{client.name}</td>
                    <td>{client.email}</td>
                    <td>{client.phone}</td>
                    <td>{client.address}</td>
                    <td>{new Date(client.created_at).toLocaleDateString('es-DO')}</td>
                  </tr>
                ))}
                {!clientsLoading && paginatedClients.length === 0 ? (
                  <tr>
                    <td colSpan="6" className="empty-row">No hay clientes para mostrar.</td>
                  </tr>
                ) : null}
              </tbody>
            </table>
          </div>

          <div className="pagination">
            <span>{sortedClients.length} clientes encontrados</span>
            <div>
              <button type="button" onClick={() => setClientPage((page) => Math.max(1, page - 1))} disabled={currentClientPage === 1}>Anterior</button>
              <strong>{currentClientPage} / {totalClientPages}</strong>
              <button type="button" onClick={() => setClientPage((page) => Math.min(totalClientPages, page + 1))} disabled={currentClientPage === totalClientPages}>Siguiente</button>
            </div>
          </div>
        </div>
      </section>
      </> : null}

      {currentPage === 'productos' ? <>
      <section id="pedidos" className="checkout">
        <div>
          <p className="eyebrow">Orden rapida</p>
          <h2>Carrito preparado para integrarse con el CRUD de ordenes.</h2>
          <p>La API incluye productos, clientes y ordenes; este panel deja lista la experiencia de compra.</p>
        </div>
        <aside className="cart">
          <h3>Pedido</h3>
          {cart.length === 0 ? <p>Agrega productos para cotizar.</p> : null}
          {cart.map((item) => (
            <div className="cart-item" key={item.id}>
              <span>{item.quantity}x {item.name}</span>
              <strong>${(item.price * item.quantity).toFixed(2)}</strong>
            </div>
          ))}
          <div className="cart-total">
            <span>Total</span>
            <strong>${total.toFixed(2)}</strong>
          </div>
          <form className="order-form" onSubmit={saveOrder}>
            <label>
              Nombre
              <input name="name" value={customer.name} onChange={updateCustomer} required minLength="2" />
            </label>
            <label>
              Email
              <input name="email" type="email" value={customer.email} onChange={updateCustomer} required />
            </label>
            <label>
              Telefono
              <input name="phone" value={customer.phone} onChange={updateCustomer} required minLength="7" />
            </label>
            <label>
              Direccion
              <textarea name="address" value={customer.address} onChange={updateCustomer} required minLength="5" />
            </label>
            <button className="save-order" type="submit" disabled={saving || cart.length === 0}>
              {saving ? 'Guardando...' : 'Salvar orden'}
            </button>
            {orderMessage ? <p className="order-message">{orderMessage}</p> : null}
          </form>
        </aside>
      </section>
      </> : null}
    </main>
  )
}

createRoot(document.getElementById('root')).render(<App />)
