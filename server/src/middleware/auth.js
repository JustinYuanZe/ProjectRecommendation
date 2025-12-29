/**
 * JWT Authentication middleware for Elysia
 * Verifies access tokens from Authorization header
 */
export const authMiddleware = (jwt) => async ({ request, set }) => {
  const authHeader = request.headers.get('authorization')
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    set.status = 401
    return { success: false, message: 'Unauthorized - No token provided' }
  }

  const token = authHeader.substring(7)
  
  try {
    const payload = await jwt.verify(token)
    
    if (!payload || payload.type !== 'access') {
      set.status = 401
      return { success: false, message: 'Invalid token type' }
    }

    // Return user info for use in route handlers
    return { userId: payload.userId, username: payload.username }
  } catch (error) {
    set.status = 401
    return { success: false, message: 'Invalid or expired token' }
  }
}

/**
 * Helper function to verify JWT and extract user info
 * Returns null if verification fails, user data if successful
 */
export const verifyToken = async (jwt, request) => {
  const authHeader = request.headers.get('authorization')
  
  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return null
  }

  const token = authHeader.substring(7)
  
  try {
    const payload = await jwt.verify(token)
    
    if (!payload || payload.type !== 'access') {
      return null
    }

    return { userId: payload.userId, username: payload.username }
  } catch (error) {
    return null
  }
}

