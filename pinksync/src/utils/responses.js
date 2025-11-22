/**
 * Standard API response wrapper
 */
export function successResponse(data, message = 'Success') {
  return {
    success: true,
    message,
    data,
  };
}

/**
 * Standard API error response
 */
export function errorResponse(message, statusCode = 500, details = null) {
  return {
    success: false,
    message,
    statusCode,
    details,
  };
}

/**
 * Pagination helper
 */
export function paginateResponse(items, page = 1, perPage = 20, total) {
  return {
    items,
    pagination: {
      page,
      perPage,
      total,
      totalPages: Math.ceil(total / perPage),
    },
  };
}
