'use client'

import { useState } from 'react'
import { Eye, EyeOff, Lock, Mail, GraduationCap } from 'lucide-react'
import { cn } from '@/lib/utils'

export default function Home() {
  const [showPassword, setShowPassword] = useState(false)
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Handle login
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: formData.email, // Use email field for login (can be registration number or email)
        password: formData.password
      })
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.role === 'ADMIN') {
        window.location.href = '/admin'
      } else {
        // Store user data in localStorage for student dashboard
        localStorage.setItem('userData', JSON.stringify(data.user))
        window.location.href = '/student'
      }
    } else {
      alert('Login failed. Please check your credentials.')
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="max-w-md w-full space-y-8">
        {/* Header */}
        <div className="text-center">
          <div className="mx-auto h-16 w-16 bg-blue-600 rounded-full flex items-center justify-center mb-4">
            <GraduationCap className="h-8 w-8 text-white" />
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            WSEI Academy Platform
          </h2>
          <p className="text-lg text-gray-600 mb-8">
            2025-2026
          </p>
        </div>

        {/* Form Card */}
        <div className="bg-white rounded-lg shadow-xl p-8">
          <div className="text-center mb-6">
            <h3 className="text-lg font-medium text-gray-900">Student & Admin Login</h3>
            <p className="text-sm text-gray-600 mt-1">Please login with your credentials</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-4">

                         <div>
               <label className="block text-sm font-medium text-gray-700 mb-1">
                 Registration Number or Email
               </label>
               <div className="relative">
                 <Mail className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                 <input
                   type="text"
                   required
                   value={formData.email}
                   onChange={(e) => setFormData({...formData, email: e.target.value})}
                   className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                   placeholder="Registration Number or Email"
                 />
               </div>
             </div>

                         <div>
               <label className="block text-sm font-medium text-gray-700 mb-1">
                 Password
               </label>
               <div className="relative">
                 <Lock className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                 <input
                   type={showPassword ? "text" : "password"}
                   required
                   value={formData.password}
                   onChange={(e) => setFormData({...formData, password: e.target.value})}
                   className="w-full pl-10 pr-10 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                   placeholder="Password"
                 />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                >
                  {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                </button>
              </div>
            </div>

                         <button
               type="submit"
               className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors"
             >
               Login
             </button>
          </form>

                     <div className="mt-4 text-center">
               <a href="#" className="text-sm text-blue-600 hover:text-blue-500">
                 Forgot Password?
               </a>
             </div>
        </div>

                 {/* Footer */}
         <div className="text-center text-sm text-gray-600">
           <p><strong>WSEI Academy</strong></p>
           <p>ul. Projektowa 4, 20-209 Lublin</p>
           <p>tel./fax: 81 749-17-70</p>
           <p>sekretariat@wsei.pl</p>
         </div>
      </div>
    </div>
  )
} 