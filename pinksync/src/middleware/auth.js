/**
 * JWT token verification middleware
 */
export async function verifyToken(request, reply) {
  try {
    const authHeader = request.headers.authorization;
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return reply.code(401).send({
        success: false,
        message: 'Missing or invalid authorization header',
      });
    }

    const token = authHeader.substring(7);
    
    // TODO: Implement actual JWT verification with config.jwt.secret
    // For now, just check if token exists
    if (!token) {
      return reply.code(401).send({
        success: false,
        message: 'Invalid token',
      });
    }
    
    // Mock user data - replace with actual JWT decode
    request.user = {
      id: 'user-123',
      email: 'user@example.com',
      role: 'developer',
    };
  } catch (error) {
    return reply.code(401).send({
      success: false,
      message: 'Token verification failed',
      details: error.message,
    });
  }
}

/**
 * Role-based access control middleware
 */
export function requireRole(...roles) {
  return async function(request, reply) {
    if (!request.user) {
      return reply.code(401).send({
        success: false,
        message: 'Authentication required',
      });
    }

    if (!roles.includes(request.user.role)) {
      return reply.code(403).send({
        success: false,
        message: 'Insufficient permissions',
      });
    }
  };
}
