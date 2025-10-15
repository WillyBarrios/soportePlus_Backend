// Ejemplo de código JavaScript para tu frontend
// Este debería funcionar ahora desde http://127.0.0.1:5500

async function testLogin() {
    try {
        const response = await fetch('http://127.0.0.1:5000/api/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                email: 'jadmin@gmail.com',
                password: 'secret123'
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Login exitoso:', data);
        
        // Guardar el token para futuras peticiones
        localStorage.setItem('access_token', data.tokens.access_token);
        
        return data;
    } catch (error) {
        console.error('Error en login:', error);
        throw error;
    }
}

// Ejemplo de uso con el token para otras peticiones
async function getCurrentUser() {
    const token = localStorage.getItem('access_token');
    
    try {
        const response = await fetch('http://127.0.0.1:5000/api/auth/me', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Usuario actual:', data);
        return data;
    } catch (error) {
        console.error('Error obteniendo usuario:', error);
        throw error;
    }
}

// Ejecutar prueba
testLogin().then(() => {
    console.log('✅ Login funcionando!');
    // Opcional: probar obtener usuario actual
    setTimeout(() => getCurrentUser(), 1000);
}).catch((error) => {
    console.error('❌ Login falló:', error);
});