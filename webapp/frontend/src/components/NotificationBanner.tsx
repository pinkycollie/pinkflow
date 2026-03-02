/**
 * Visual Notification Banner Component
 * 
 * Deaf-First Design:
 * - Visual notifications without audio
 * - Clear, persistent banners for important events
 * - IoT device notifications with Vibration API support
 * - Real-time updates via PubSub system
 */

import React, { useState, useEffect } from 'react';

interface Notification {
  id: string;
  type: 'info' | 'success' | 'warning' | 'error';
  title: string;
  message: string;
  priority: 'low' | 'normal' | 'high' | 'urgent';
  duration?: number;
  icon?: string;
  animation?: 'fade' | 'slide' | 'bounce' | 'pulse';
  dismissible?: boolean;
}

interface NotificationBannerProps {
  notifications?: Notification[];
  onDismiss?: (id: string) => void;
  enableVibration?: boolean;
}

const NotificationBanner: React.FC<NotificationBannerProps> = ({
  notifications = [],
  onDismiss,
  enableVibration = false
}) => {
  const [activeNotifications, setActiveNotifications] = useState<Notification[]>(notifications);

  useEffect(() => {
    setActiveNotifications(notifications);
  }, [notifications]);

  useEffect(() => {
    // Auto-dismiss notifications with duration
    const timers: NodeJS.Timeout[] = [];
    
    activeNotifications.forEach(notification => {
      if (notification.duration && notification.duration > 0) {
        const timer = setTimeout(() => {
          handleDismiss(notification.id);
        }, notification.duration);
        timers.push(timer);
      }
    });

    return () => {
      timers.forEach(timer => clearTimeout(timer));
    };
  }, [activeNotifications]);

  useEffect(() => {
    // Trigger vibration for high priority notifications
    if (enableVibration && 'vibrate' in navigator) {
      activeNotifications.forEach(notification => {
        if (notification.priority === 'high' || notification.priority === 'urgent') {
          const pattern = getVibrationPattern(notification.priority);
          navigator.vibrate(pattern);
        }
      });
    }
  }, [activeNotifications, enableVibration]);

  const getVibrationPattern = (priority: string): number[] => {
    switch (priority) {
      case 'low':
        return [100];
      case 'normal':
        return [200, 100, 200];
      case 'high':
        return [300, 100, 300, 100, 300];
      case 'urgent':
        return [500, 200, 500, 200, 500, 200, 500];
      default:
        return [200];
    }
  };

  const handleDismiss = (id: string) => {
    setActiveNotifications(prev => prev.filter(n => n.id !== id));
    if (onDismiss) {
      onDismiss(id);
    }
  };

  const getNotificationStyle = (notification: Notification): string => {
    const baseClasses = 'rounded-lg shadow-lg p-4 mb-3 flex items-start justify-between';
    const animationClasses = getAnimationClass(notification.animation);
    
    switch (notification.type) {
      case 'success':
        return `${baseClasses} ${animationClasses} bg-green-100 border-l-4 border-green-500 text-green-900`;
      case 'warning':
        return `${baseClasses} ${animationClasses} bg-yellow-100 border-l-4 border-yellow-500 text-yellow-900`;
      case 'error':
        return `${baseClasses} ${animationClasses} bg-red-100 border-l-4 border-red-500 text-red-900`;
      case 'info':
      default:
        return `${baseClasses} ${animationClasses} bg-blue-100 border-l-4 border-blue-500 text-blue-900`;
    }
  };

  const getAnimationClass = (animation?: string): string => {
    switch (animation) {
      case 'fade':
        return 'animate-fade-in';
      case 'slide':
        return 'animate-slide-in';
      case 'bounce':
        return 'animate-bounce-in';
      case 'pulse':
        return 'animate-pulse';
      default:
        return 'animate-fade-in';
    }
  };

  const getIcon = (notification: Notification): string => {
    if (notification.icon) {
      return notification.icon;
    }
    
    switch (notification.type) {
      case 'success':
        return '✅';
      case 'warning':
        return '⚠️';
      case 'error':
        return '🚨';
      case 'info':
      default:
        return 'ℹ️';
    }
  };

  if (activeNotifications.length === 0) {
    return null;
  }

  return (
    <div className="fixed top-4 right-4 z-50 max-w-md w-full space-y-2" role="alert" aria-live="polite">
      {activeNotifications.map(notification => (
        <div key={notification.id} className={getNotificationStyle(notification)}>
          <div className="flex items-start flex-grow">
            <span className="text-2xl mr-3" aria-hidden="true">
              {getIcon(notification)}
            </span>
            <div className="flex-grow">
              <h4 className="font-bold text-lg mb-1">{notification.title}</h4>
              <p className="text-sm">{notification.message}</p>
              {notification.priority === 'urgent' && (
                <p className="text-xs mt-2 font-semibold">URGENT: Requires immediate attention</p>
              )}
            </div>
          </div>
          {(notification.dismissible !== false) && (
            <button
              onClick={() => handleDismiss(notification.id)}
              className="ml-4 text-2xl font-bold hover:opacity-75 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
              aria-label="Dismiss notification"
            >
              ×
            </button>
          )}
        </div>
      ))}
      
      {/* Screen reader announcement */}
      <div className="sr-only" role="status" aria-live="polite">
        {activeNotifications.length > 0 && (
          `${activeNotifications.length} notification${activeNotifications.length > 1 ? 's' : ''} displayed`
        )}
      </div>
    </div>
  );
};

export default NotificationBanner;

// Hook for managing notifications
export const useNotifications = () => {
  const [notifications, setNotifications] = useState<Notification[]>([]);

  const addNotification = (notification: Omit<Notification, 'id'>) => {
    const id = `notification-${Date.now()}-${Math.random()}`;
    const newNotification: Notification = {
      id,
      ...notification,
      dismissible: notification.dismissible !== false
    };
    
    setNotifications(prev => [...prev, newNotification]);
    return id;
  };

  const removeNotification = (id: string) => {
    setNotifications(prev => prev.filter(n => n.id !== id));
  };

  const clearAll = () => {
    setNotifications([]);
  };

  return {
    notifications,
    addNotification,
    removeNotification,
    clearAll
  };
};

// Example usage:
/*
const MyComponent = () => {
  const { notifications, addNotification, removeNotification } = useNotifications();

  const handleTestComplete = () => {
    addNotification({
      type: 'success',
      title: 'Test Completed',
      message: 'Model test finished with 95% accuracy',
      priority: 'high',
      duration: 5000,
      animation: 'bounce'
    });
  };

  return (
    <>
      <NotificationBanner 
        notifications={notifications}
        onDismiss={removeNotification}
        enableVibration={true}
      />
      <button onClick={handleTestComplete}>Run Test</button>
    </>
  );
};
*/
