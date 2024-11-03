import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Orders = () => {
    const [orders, setOrders] = useState([]);

    useEffect(() => {
        const fetchOrders = async () => {
            try {

                const response = await axios.get(`${process.env.BACKEND_URL}/api/orders`);
                setOrders(response.data);
            } catch (error) {
                console.error("Error fetching orders", error);
            }
        };

        fetchOrders();
    }, []);

    return (
        <div>
            <h1>Pedidos</h1>
            <ul>
                {orders.map(order => (
                    <li key={order.id}>
                        Número de Orden: {order.number} - Total: {order.total}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default Orders;