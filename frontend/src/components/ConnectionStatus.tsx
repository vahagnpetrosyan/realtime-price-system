import React from 'react';
import { ConnectionStatus as Status } from '../types';

interface ConnectionStatusProps {
  status: Status;
}

export const ConnectionStatus: React.FC<ConnectionStatusProps> = ({ status }) => {
  const getStatusClass = () => {
    switch (status) {
      case Status.CONNECTED:
        return 'status-connected';
      case Status.CONNECTING:
        return 'status-connecting';
      case Status.ERROR:
        return 'status-error';
      default:
        return 'status-disconnected';
    }
  };


  return (
    <div className={`connection-status ${getStatusClass()}`}>
      <span className="status-indicator"></span>
    </div>
  );
};