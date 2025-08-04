'use client'

import { useState, useEffect } from 'react'
import { LogOut, Users, Search, ArrowUpDown, Filter, GraduationCap, Mail, Phone, Trash2 } from 'lucide-react'

interface Student {
  id: string
  registrationNo: string
  firstName: string
  lastName: string
  courseOfStudy: string
  semester: number
  email: string
  phone?: string
  status: string
  enrollmentDate: string
}

type SortField = 'registrationNo' | 'firstName' | 'lastName' | 'courseOfStudy' | 'semester' | 'enrollmentDate'
type SortDirection = 'asc' | 'desc'

export default function AdminDashboard() {
  const [students, setStudents] = useState<Student[]>([])
  const [filteredStudents, setFilteredStudents] = useState<Student[]>([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [sortField, setSortField] = useState<SortField>('registrationNo')
  const [sortDirection, setSortDirection] = useState<SortDirection>('asc')
  const [courseFilter, setCourseFilter] = useState('')
  const [semesterFilter, setSemesterFilter] = useState('')
  const [deletingStudent, setDeletingStudent] = useState<string | null>(null)
  const [showDeleteConfirm, setShowDeleteConfirm] = useState<{id: string, name: string} | null>(null)
  const [showRegistrationModal, setShowRegistrationModal] = useState(false)
  const [registrationForm, setRegistrationForm] = useState({
    firstName: '',
    lastName: '',
    dateOfBirth: '',
    courseOfStudy: '',
    semester: ''
  })
  const [registeringStudent, setRegisteringStudent] = useState(false)

  const fetchStudents = async () => {
    try {
      console.log('🔍 Frontend: Fetching students from API...')
      const response = await fetch('/api/students')
      
      console.log('🔍 Frontend: Response status:', response.status)
      
      if (!response.ok) {
        throw new Error(`Failed to fetch students: ${response.status}`)
      }
      
      const data = await response.json()
      console.log('🔍 Frontend: Response data:', data)
      
      if (data.success && data.students) {
        console.log(`✅ Frontend: Setting ${data.students.length} students`)
        setStudents(data.students)
        setFilteredStudents(data.students)
      } else {
        throw new Error('Invalid response format')
      }
      
      setLoading(false)
    } catch (error) {
      console.error('❌ Frontend: Error fetching students:', error)
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchStudents()
  }, [])

  useEffect(() => {
    let filtered = students

    // Apply search filter
    if (searchTerm) {
      filtered = filtered.filter(student =>
        student.firstName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        student.lastName.toLowerCase().includes(searchTerm.toLowerCase()) ||
        student.registrationNo.toLowerCase().includes(searchTerm.toLowerCase()) ||
        student.email.toLowerCase().includes(searchTerm.toLowerCase())
      )
    }

    // Apply course filter
    if (courseFilter) {
      filtered = filtered.filter(student => student.courseOfStudy === courseFilter)
    }

    // Apply semester filter
    if (semesterFilter) {
      filtered = filtered.filter(student => student.semester.toString() === semesterFilter)
    }

    // Apply sorting
    filtered.sort((a, b) => {
      let aValue: any = a[sortField]
      let bValue: any = b[sortField]

      if (sortField === 'firstName' || sortField === 'lastName') {
        aValue = `${a.firstName} ${a.lastName}`
        bValue = `${b.firstName} ${b.lastName}`
      }

      if (typeof aValue === 'string') {
        aValue = aValue.toLowerCase()
        bValue = bValue.toLowerCase()
      }

      if (aValue < bValue) return sortDirection === 'asc' ? -1 : 1
      if (aValue > bValue) return sortDirection === 'asc' ? 1 : -1
      return 0
    })

    setFilteredStudents(filtered)
  }, [students, searchTerm, courseFilter, semesterFilter, sortField, sortDirection])

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc')
    } else {
      setSortField(field)
      setSortDirection('asc')
    }
  }

  const handleLogout = () => {
    // Clear any stored data and redirect to login
    localStorage.removeItem('userData')
    window.location.href = '/'
  }

  const handleDeleteStudent = async (studentId: string, studentName: string) => {
    setShowDeleteConfirm({ id: studentId, name: studentName })
  }

  const confirmDelete = async () => {
    if (!showDeleteConfirm) return

    setDeletingStudent(showDeleteConfirm.id)
    setShowDeleteConfirm(null)

    try {
      const response = await fetch(`/api/students/${showDeleteConfirm.id}`, {
        method: 'DELETE'
      })

      if (response.ok) {
        // Remove the student from the local state
        setStudents(students.filter(s => s.id !== showDeleteConfirm.id))
        setFilteredStudents(filteredStudents.filter(s => s.id !== showDeleteConfirm.id))
        alert('Student deleted successfully')
      } else {
        const error = await response.json()
        alert(`Failed to delete student: ${error.message}`)
      }
    } catch (error) {
      console.error('Error deleting student:', error)
      alert('Failed to delete student. Please try again.')
    } finally {
      setDeletingStudent(null)
    }
  }

  const cancelDelete = () => {
    setShowDeleteConfirm(null)
  }

  const handleRegisterStudent = async () => {
    if (!registrationForm.firstName || !registrationForm.lastName || !registrationForm.dateOfBirth || 
        !registrationForm.courseOfStudy || !registrationForm.semester) {
      alert('All fields are required')
      return
    }

    setRegisteringStudent(true)

    try {
      // Generate email and password based on name
      const cleanFirstName = registrationForm.firstName.toLowerCase().replace(/[^a-z]/g, '')
      const cleanLastName = registrationForm.lastName.toLowerCase().replace(/[^a-z]/g, '')
      const email = `${cleanFirstName}.${cleanLastName}@student.wsei.pl`
      const password = `${cleanFirstName}@123`

      const response = await fetch('/api/auth/signup', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...registrationForm,
          email,
          password
        })
      })

      if (response.ok) {
        const data = await response.json()
        alert(`Student registered successfully!\nRegistration Number: ${data.registrationNo}\nEmail: ${email}\nPassword: ${password}`)
        
        // Reset form and close modal
        setRegistrationForm({
          firstName: '',
          lastName: '',
          dateOfBirth: '',
          courseOfStudy: '',
          semester: ''
        })
        setShowRegistrationModal(false)
        
        // Refresh student list
        await fetchStudents()
      } else {
        const error = await response.json()
        alert(`Registration failed: ${error.message}`)
      }
    } catch (error) {
      console.error('Error registering student:', error)
      alert('Failed to register student. Please try again.')
    } finally {
      setRegisteringStudent(false)
    }
  }

  const cancelRegistration = () => {
    setShowRegistrationModal(false)
    setRegistrationForm({
      firstName: '',
      lastName: '',
      dateOfBirth: '',
      courseOfStudy: '',
      semester: ''
    })
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    })
  }

  const getStatusBadge = (status: string) => {
    const statusConfig = {
      'ACTIVE': { label: 'Active', class: 'bg-green-100 text-green-800' },
      'INACTIVE': { label: 'Inactive', class: 'bg-red-100 text-red-800' },
      'SUSPENDED': { label: 'Suspended', class: 'bg-yellow-100 text-yellow-800' }
    }
    
    const config = statusConfig[status as keyof typeof statusConfig] || statusConfig['INACTIVE']
    
    return (
      <span className={`px-2 py-1 rounded-full text-xs font-medium ${config.class}`}>
        {config.label}
      </span>
    )
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

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <div className="h-10 w-10 bg-blue-600 rounded-full flex items-center justify-center">
                <Users className="h-6 w-6 text-white" />
              </div>
              <div className="ml-3">
                <h1 className="text-xl font-semibold text-gray-900">
                  WSEI Academy Platform
                </h1>
                <p className="text-sm text-gray-500">Admin Panel</p>
              </div>
            </div>
            <div className="flex items-center space-x-3">
              <button
                onClick={() => setShowRegistrationModal(true)}
                className="flex items-center px-4 py-2 text-sm font-medium text-white bg-green-600 border border-green-600 rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
              >
                <Users className="h-4 w-4 mr-2" />
                Register New Student
              </button>
              <button
                onClick={handleLogout}
                className="flex items-center px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="h-12 w-12 bg-blue-100 rounded-lg flex items-center justify-center">
                <Users className="h-6 w-6 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">All Students</p>
                <p className="text-2xl font-bold text-gray-900">{students.length}</p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="h-12 w-12 bg-green-100 rounded-lg flex items-center justify-center">
                <Users className="h-6 w-6 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Active</p>
                <p className="text-2xl font-bold text-gray-900">
                  {students.filter(s => s.status === 'ACTIVE').length}
                </p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="h-12 w-12 bg-purple-100 rounded-lg flex items-center justify-center">
                <GraduationCap className="h-6 w-6 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">Courses</p>
                <p className="text-2xl font-bold text-gray-900">
                  {new Set(students.map(s => s.courseOfStudy)).size}
                </p>
              </div>
            </div>
          </div>
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="h-12 w-12 bg-orange-100 rounded-lg flex items-center justify-center">
                <Users className="h-6 w-6 text-orange-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-600">New (2025)</p>
                <p className="text-2xl font-bold text-gray-900">
                  {students.filter(s => s.registrationNo.includes('2025')).length}
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Filters and Search */}
        <div className="bg-white rounded-lg shadow-md p-6 mb-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="relative">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
              <input
                type="text"
                placeholder="Search students..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
              />
            </div>
            <select
              value={courseFilter}
              onChange={(e) => setCourseFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
            >
              <option value="" className="text-gray-500">All Courses</option>
              {Array.from(new Set(students.map(s => s.courseOfStudy))).map(course => (
                <option key={course} value={course} className="text-gray-900">{course}</option>
              ))}
            </select>
            <select
              value={semesterFilter}
              onChange={(e) => setSemesterFilter(e.target.value)}
              className="px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
            >
              <option value="" className="text-gray-500">All Semesters</option>
              {Array.from(new Set(students.map(s => s.semester))).sort().map(semester => (
                <option key={semester} value={semester.toString()} className="text-gray-900">Semester {semester}</option>
              ))}
            </select>
            <div className="text-sm text-gray-600 flex items-center">
              <Filter className="h-4 w-4 mr-2" />
              Found: {filteredStudents.length} students
            </div>
          </div>
        </div>

        {/* Students Table */}
        <div className="bg-white rounded-lg shadow-md overflow-hidden">
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('registrationNo')}
                  >
                    <div className="flex items-center">
                      Registration Number
                      <ArrowUpDown className="h-4 w-4 ml-1" />
                    </div>
                  </th>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('firstName')}
                  >
                    <div className="flex items-center">
                      Full Name
                      <ArrowUpDown className="h-4 w-4 ml-1" />
                    </div>
                  </th>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('courseOfStudy')}
                  >
                    <div className="flex items-center">
                      Course
                      <ArrowUpDown className="h-4 w-4 ml-1" />
                    </div>
                  </th>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('semester')}
                  >
                    <div className="flex items-center">
                      Semester
                      <ArrowUpDown className="h-4 w-4 ml-1" />
                    </div>
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Email
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Phone
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Status
                  </th>
                  <th 
                    className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-100"
                    onClick={() => handleSort('enrollmentDate')}
                  >
                    <div className="flex items-center">
                      Enrollment Date
                      <ArrowUpDown className="h-4 w-4 ml-1" />
                    </div>
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredStudents.map((student) => (
                  <tr key={student.id} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-mono text-gray-900">{student.registrationNo}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">
                        {student.firstName} {student.lastName}
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{student.courseOfStudy}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{student.semester}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <Mail className="h-4 w-4 text-gray-400 mr-2" />
                        <div className="text-sm text-gray-900">{student.email}</div>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {student.phone ? (
                        <div className="flex items-center">
                          <Phone className="h-4 w-4 text-gray-400 mr-2" />
                          <div className="text-sm text-gray-900">{student.phone}</div>
                        </div>
                      ) : (
                        <div className="text-sm text-gray-500">-</div>
                      )}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      {getStatusBadge(student.status)}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{formatDate(student.enrollmentDate)}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <button
                        onClick={() => handleDeleteStudent(student.id, `${student.firstName} ${student.lastName}`)}
                        disabled={deletingStudent === student.id}
                        className={`transition-colors ${
                          deletingStudent === student.id 
                            ? 'text-gray-400 cursor-not-allowed' 
                            : 'text-red-600 hover:text-red-900'
                        }`}
                        title="Delete student"
                      >
                        {deletingStudent === student.id ? (
                          <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-red-600"></div>
                        ) : (
                          <Trash2 className="h-4 w-4" />
                        )}
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          
          {filteredStudents.length === 0 && (
            <div className="text-center py-12">
              <Users className="h-12 w-12 text-gray-400 mx-auto mb-4" />
              <p className="text-gray-500">No students found matching the search criteria.</p>
            </div>
          )}
        </div>
      </div>

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Confirm Delete</h3>
            <p className="text-gray-600 mb-6">
              Are you sure you want to delete <strong>{showDeleteConfirm.name}</strong>? 
              This action cannot be undone and will permanently remove the student from the database.
            </p>
            <div className="flex justify-end space-x-3">
              <button
                onClick={cancelDelete}
                className="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={confirmDelete}
                className="px-4 py-2 bg-red-600 text-white rounded-md hover:bg-red-700 transition-colors"
              >
                Delete
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Registration Modal */}
      {showRegistrationModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[9999]">
          <div className="bg-white rounded-lg p-6 max-w-md w-full mx-4 max-h-[90vh] overflow-y-auto">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Register New Student</h3>
            
            <div className="space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                  <input
                    type="text"
                    required
                    value={registrationForm.firstName}
                    onChange={(e) => setRegistrationForm({...registrationForm, firstName: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                    placeholder="First Name"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                  <input
                    type="text"
                    required
                    value={registrationForm.lastName}
                    onChange={(e) => setRegistrationForm({...registrationForm, lastName: e.target.value})}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                    placeholder="Last Name"
                  />
                </div>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Date of Birth</label>
                <input
                  type="date"
                  required
                  value={registrationForm.dateOfBirth}
                  onChange={(e) => setRegistrationForm({...registrationForm, dateOfBirth: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Course of Study</label>
                <select
                  required
                  value={registrationForm.courseOfStudy}
                  onChange={(e) => setRegistrationForm({...registrationForm, courseOfStudy: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                >
                  <option value="" className="text-gray-500">Select Course</option>
                  <option value="Computer Science" className="text-gray-900">Computer Science</option>
                  <option value="Management" className="text-gray-900">Management</option>
                  <option value="Economics" className="text-gray-900">Economics</option>
                  <option value="Law" className="text-gray-900">Law</option>
                  <option value="Psychology" className="text-gray-900">Psychology</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Semester</label>
                <select
                  required
                  value={registrationForm.semester}
                  onChange={(e) => setRegistrationForm({...registrationForm, semester: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-900"
                >
                  <option value="" className="text-gray-500">Select Semester</option>
                  <option value="1" className="text-gray-900">Semester 1</option>
                  <option value="2" className="text-gray-900">Semester 2</option>
                  <option value="3" className="text-gray-900">Semester 3</option>
                  <option value="4" className="text-gray-900">Semester 4</option>
                  <option value="5" className="text-gray-900">Semester 5</option>
                  <option value="6" className="text-gray-900">Semester 6</option>
                </select>
              </div>

              {registrationForm.firstName && registrationForm.lastName && (
                <div className="bg-blue-50 p-3 rounded-md">
                  <p className="text-sm text-blue-800">
                    <strong>Auto-generated credentials:</strong><br />
                    <strong>Email:</strong> {registrationForm.firstName.toLowerCase().replace(/[^a-z]/g, '')}.{registrationForm.lastName.toLowerCase().replace(/[^a-z]/g, '')}@student.wsei.pl<br />
                    <strong>Password:</strong> {registrationForm.firstName.toLowerCase().replace(/[^a-z]/g, '')}@123
                  </p>
                </div>
              )}
            </div>

            <div className="flex justify-end space-x-3 mt-6">
              <button
                onClick={cancelRegistration}
                disabled={registeringStudent}
                className="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 transition-colors disabled:opacity-50"
              >
                Cancel
              </button>
              <button
                onClick={handleRegisterStudent}
                disabled={registeringStudent}
                className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors disabled:opacity-50"
              >
                {registeringStudent ? 'Registering...' : 'Register Student'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
} 