'use client'

import { useState, useEffect } from 'react'
import { LogOut, User, Calendar, BookOpen, GraduationCap, Mail, Phone, MapPin, CreditCard } from 'lucide-react'

interface StudentData {
  id: string
  registrationNo: string
  firstName: string
  lastName: string
  dateOfBirth: string
  courseOfStudy: string
  semester: number
  email: string
  phone?: string
  address?: string
  enrollmentDate: string
  status: string
}

export default function StudentDashboard() {
  const [studentData, setStudentData] = useState<StudentData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchStudentData = async () => {
      try {
        // Get user data from localStorage
        const userDataString = localStorage.getItem('userData')
        if (!userDataString) {
          throw new Error('No user data found')
        }
        
        const userData = JSON.parse(userDataString)
        
        // Fetch student data from API with user ID
        const response = await fetch(`/api/student/profile?userId=${userData.id}`)
        
        if (!response.ok) {
          throw new Error('Failed to fetch student data')
        }
        
        const data = await response.json()
        
        if (data.success && data.student) {
          setStudentData(data.student)
        } else {
          throw new Error('Invalid response format')
        }
        
        setLoading(false)
      } catch (error) {
        console.error('Error fetching student data:', error)
        setLoading(false)
      }
    }

    fetchStudentData()
  }, [])

  const handleLogout = () => {
    // Clear localStorage and redirect to login
    localStorage.removeItem('userData')
    window.location.href = '/'
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('pl-PL')
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
                 <div className="text-center">
           <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
           <p className="mt-4 text-gray-600">Loading data...</p>
         </div>
      </div>
    )
  }

  if (!studentData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Failed to load student data.</p>
          <p className="text-sm text-gray-500 mt-2">Please login again.</p>
          <button 
            onClick={() => window.location.href = '/'}
            className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
          >
            Go to Login
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <div className="h-10 w-10 bg-blue-600 rounded-full flex items-center justify-center">
                <GraduationCap className="h-6 w-6 text-white" />
              </div>
                             <div className="ml-3">
                 <h1 className="text-xl font-semibold text-gray-900">
                   WSEI E-Learning Platform
                 </h1>
                 <p className="text-sm text-gray-500">Student Panel</p>
               </div>
            </div>
            <button
              onClick={handleLogout}
              className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
                             <LogOut className="h-4 w-4 mr-2" />
               Logout
            </button>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Section */}
        <div className="bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg shadow-lg p-6 mb-8">
          <div className="flex items-center">
            <div className="h-16 w-16 bg-white bg-opacity-20 rounded-full flex items-center justify-center">
              <User className="h-8 w-8 text-white" />
            </div>
            <div className="ml-4">
                           <h2 className="text-2xl font-bold text-white">
               Welcome, {studentData.firstName} {studentData.lastName}!
             </h2>
             <p className="text-blue-100">
               Registration Number: {studentData.registrationNo}
             </p>
            </div>
          </div>
        </div>

        {/* Student Information Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Personal Information */}
          <div className="bg-white rounded-lg shadow-md p-6">
                         <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
               <User className="h-5 w-5 mr-2 text-blue-600" />
               Personal Information
             </h3>
            <div className="space-y-4">
                             <div className="flex justify-between items-center py-2 border-b border-gray-100">
                 <span className="text-gray-600">Full Name:</span>
                 <span className="font-medium">{studentData.firstName} {studentData.lastName}</span>
               </div>
               <div className="flex justify-between items-center py-2 border-b border-gray-100">
                 <span className="text-gray-600">Date of Birth:</span>
                 <span className="font-medium">{formatDate(studentData.dateOfBirth)}</span>
               </div>
               <div className="flex justify-between items-center py-2 border-b border-gray-100">
                 <span className="text-gray-600">Email:</span>
                 <span className="font-medium">{studentData.email}</span>
               </div>
               {studentData.phone && (
                 <div className="flex justify-between items-center py-2 border-b border-gray-100">
                   <span className="text-gray-600">Phone:</span>
                   <span className="font-medium">{studentData.phone}</span>
                 </div>
               )}
               {studentData.address && (
                 <div className="flex justify-between items-center py-2">
                   <span className="text-gray-600">Address:</span>
                   <span className="font-medium text-right">{studentData.address}</span>
                 </div>
               )}
            </div>
          </div>

          {/* Academic Information */}
          <div className="bg-white rounded-lg shadow-md p-6">
                         <h3 className="text-lg font-semibold text-gray-900 mb-4 flex items-center">
               <GraduationCap className="h-5 w-5 mr-2 text-blue-600" />
               Academic Information
             </h3>
            <div className="space-y-4">
                             <div className="flex justify-between items-center py-2 border-b border-gray-100">
                 <span className="text-gray-600">Registration Number:</span>
                 <span className="font-medium font-mono">{studentData.registrationNo}</span>
               </div>
               <div className="flex justify-between items-center py-2 border-b border-gray-100">
                 <span className="text-gray-600">Course of Study:</span>
                 <span className="font-medium">{studentData.courseOfStudy}</span>
               </div>
               <div className="flex justify-between items-center py-2 border-b border-gray-100">
                 <span className="text-gray-600">Semester:</span>
                 <span className="font-medium">{studentData.semester}</span>
               </div>
               <div className="flex justify-between items-center py-2 border-b border-gray-100">
                 <span className="text-gray-600">Enrollment Date:</span>
                 <span className="font-medium">{formatDate(studentData.enrollmentDate)}</span>
               </div>
               <div className="flex justify-between items-center py-2">
                 <span className="text-gray-600">Status:</span>
                 <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                   studentData.status === 'ACTIVE' 
                     ? 'bg-green-100 text-green-800' 
                     : 'bg-red-100 text-red-800'
                 }`}>
                   {studentData.status === 'ACTIVE' ? 'Active' : 'Inactive'}
                 </span>
               </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
                 <div className="mt-8 bg-white rounded-lg shadow-md p-6">
           <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
           <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
             <button className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
               <BookOpen className="h-5 w-5 mr-3 text-blue-600" />
               <span className="text-sm font-medium">My Courses</span>
             </button>
             <button className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
               <Calendar className="h-5 w-5 mr-3 text-blue-600" />
               <span className="text-sm font-medium">Schedule</span>
             </button>
             <button className="flex items-center p-4 border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors">
               <CreditCard className="h-5 w-5 mr-3 text-blue-600" />
               <span className="text-sm font-medium">Fees</span>
             </button>
           </div>
         </div>
      </div>
    </div>
  )
} 