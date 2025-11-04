import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Database, Download, ArrowRightCircle, CheckCircle } from 'lucide-react';

const steps = [
  { id: 1, name: 'Analyze', path: '/', icon: Database },
  { id: 2, name: 'Extract', path: '/extract', icon: Download },
  { id: 3, name: 'Migrate', path: '/migrate', icon: ArrowRightCircle },
  { id: 4, name: 'Reconcile', path: '/reconcile', icon: CheckCircle },
];

const Sidebar = () => {
  const location = useLocation();

  return (
    <div className="w-64 bg-white shadow-md flex flex-col">
      <div className="p-6 border-b">
        <h1 className="text-xl font-bold text-[#085690]">Strata</h1>
        <p className="text-sm text-gray-500">Enterprise AI Translation Platform</p>
      </div>
      
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {steps.map((step) => {
            const Icon = step.icon;
            const isActive = location.pathname === step.path;
            
            return (
              <li key={step.id}>
                <Link
                  to={step.path}
                  className={`flex items-center p-3 rounded-lg transition-colors ${
                    isActive 
                      ? 'bg-[#085690] text-white' 
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <Icon className="h-5 w-5 mr-3" />
                  <span className="font-medium">{step.id}. {step.name}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>
      
      <div className="p-4 border-t text-xs text-gray-500">
        <p>AI-Powered Database Migration</p>
      </div>
    </div>
  );
};

export default Sidebar;