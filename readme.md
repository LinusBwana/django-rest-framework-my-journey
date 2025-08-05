# Django REST Framework Learning Project
A comprehensive Django REST Framework (DRF) project demonstrating various API development patterns, from function-based views to advanced ViewSets with filtering and pagination.

## Project Overview
This project serves as a hands-on exploration of Django REST Framework concepts, implementing multiple approaches to API development using Student, Employee, and Blog models. The project showcases the evolution from basic function-based views to sophisticated class-based views and ViewSets.

## What is an API?
API stands for Application Programming Interface  
It acts as a two-way communication bridge between frontend and backend

## What is REST API
- *Rest* stands for Representational State Transfer
- It organizes how the web applications talk to each other, separating what the user sees (frontend) and what runs behind the scenes (backend). 

## Core Principles of REST
1. **Stateless:** The server does not store any information about the client between requests.
2. **Client-Server Architecture:** The app (client) asks for things (data) and the server does what's requested (sends data or makes changes).
3. **Standardized Interface:** REST APIs rely on a set of standard methods (GET, POST, PUT, ,PATCH, DELETE) for interacting with resources (*RESTful Operations*).
     - GET - Retrieve data (e.g., fetch a list or item)
     - POST - Create a new resource
     - PUT - Update an entire existing resource
     - PATCH - Partially update an existing resource
     - DELETE - Delete a resource
4. **Easy-to-Read Data:** REST APIs returns the response in a standardized easy to read formats, typically JSON or XML formats.
 

## What I Built

### Core Applications

#### 1. **API App** - Main API Logic
- **Students API**: Function-based views for CRUD operations
- **Employees API**: Multiple implementations using different DRF patterns
- **Blog & Comments API**: Advanced features with filtering and pagination

#### 2. **Students App** 
- Basic model structure for student data
- Integration with function-based API views

#### 3. **Employees App**
- Employee model for demonstrating various view patterns
- Used across multiple API implementations

#### 4. **Blogs App**
- Blog and Comment models with foreign key relationships
- Advanced filtering and search capabilities

## API Implementations & Patterns Learnt

### 1. Function-Based Views (FBV) - The Foundation
**Endpoints**: 
- `GET/POST /students/` - List all students or create new ones
- `GET/PUT/PATCH/DELETE /student/<int:pk>/` - Individual student operations

**URL Configuration:**
```python
# urls.py
urlpatterns = [
    path('students/', views.studentsView),
    path('student/<int:pk>/', views.studentDetailView),
]
```

**Implementation:**
```python
# views.py
@api_view(['GET', 'POST'])
def studentsView(request):
    if request.method == 'GET':
        # Get all data from the Student table
        students = Student.objects.all().order_by('id')
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        many = isinstance(request.data, list)  # Handle bulk creation
        serializer = StudentSerializer(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])  
def studentDetailView(request, pk):
    try:
        student = Student.objects.get(pk=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = StudentSerializer(student)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT':
        serializer = StudentSerializer(student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'PATCH':
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        student.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

**Key Learning**: 
- **Manual Control**: Complete control over request handling and response formatting
- **@api_view Decorator**: Converts functions into DRF API views
- **Bulk Operations**: Handling both single and multiple object creation
- **Error Handling**: Manual exception handling and appropriate HTTP status codes
- **Partial Updates**: PATCH vs PUT implementation differences

---

### 2. Class-Based Views (CBV) - Object-Oriented Approach
**Endpoints**: 
- `GET/POST /employees/` - List employees or create new ones
- `GET/PUT/PATCH/DELETE /employees/<int:pk>/` - Individual employee operations

**URL Configuration:**
```python
# urls.py
urlpatterns = [
    path('employees/', views.Employees.as_view()),
    path('employees/<int:pk>/', views.EmployeeDetail.as_view()),
]
```

**Implementation:**
```python
# views.py
class Employees(APIView):
    def get(self, request):
        employees = Employee.objects.all().order_by('emp_name')
        serializer = EmployeeSerializer(employees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        many = isinstance(request.data, list)
        serializer = EmployeeSerializer(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetail(APIView):
    def get_object(self, pk):
        try:
            return Employee.objects.get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        employee = self.get_object(pk)
        serializer = EmployeeSerializer(employee, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

**Key Learning**:
- **OOP Benefits**: Better code organization and inheritance possibilities
- **Method Separation**: Each HTTP method has its own class method
- **Helper Methods**: `get_object()` method for DRY principle
- **Exception Handling**: Using `Http404` for cleaner error handling
- **Class-based Structure**: More maintainable and extensible code

---

### 3. Mixins - Modular Functionality
**Endpoints**: 
- `GET/POST /staffs/` - Staff list and creation
- `GET/PUT/DELETE /staffs/<int:pk>/` - Individual staff operations

**URL Configuration:**
```python
# urls.py
urlpatterns = [
    path('staffs/', views.Staffs.as_view()),
    path('staffs/<int:pk>/', views.StaffDetails.as_view()),
]
```

**Implementation:**
```python
# views.py
class Staffs(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request):
        return self.list(request)  # Delegate to ListModelMixin
    
    def post(self, request):
        return self.create(request)  # Delegate to CreateModelMixin

class StaffDetails(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, 
                   mixins.DestroyModelMixin, generics.GenericAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get(self, request, pk):
        return self.retrieve(request, pk)  # Delegate to RetrieveModelMixin
    
    def put(self, request, pk):
        return self.update(request, pk)  # Delegate to UpdateModelMixin
    
    def delete(self, request, pk):
        return self.destroy(request, pk)  # Delegate to DestroyModelMixin
```

**Key Learning**:
- **Mixin Composition**: Combining multiple behaviors through inheritance
- **DRY Principle**: Reusing common CRUD functionality
- **Delegation Pattern**: Views delegate to mixin methods
- **Declarative Configuration**: `queryset` and `serializer_class` attributes
- **Less Boilerplate**: Reduced code repetition while maintaining flexibility

---

### 4. Generic Views - Maximum Efficiency
**Endpoints**: 
- `GET/POST /workers/` - Worker list and creation
- `GET/PUT/PATCH/DELETE /workers/<int:pk>/` - Individual worker operations

**URL Configuration:**
```python
# urls.py
urlpatterns = [
    path('workers/', views.Workers.as_view()),
    path('workers/<int:pk>/', views.WorkerDetails.as_view()),
]
```

**Implementation:**
```python
# views.py
class Workers(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

class WorkerDetails(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_field = 'pk'
```

**Key Learning**:
- **Minimal Code**: Maximum functionality with minimal lines of code
- **Convention over Configuration**: Follows REST conventions automatically
- **Built-in CRUD**: All CRUD operations handled by DRF
- **Lookup Fields**: Customizable object lookup strategies
- **Best for Standard APIs**: Perfect for typical REST API patterns

---

### 5. ViewSets - The Ultimate Abstraction
**Endpoints**: 
- **AgentViewset** (Manual ViewSet):
  - `GET /agents/` - List all agents
  - `POST /agents/` - Create new agent
  - `GET /agents/<id>/` - Retrieve specific agent
  - `PUT /agents/<id>/` - Update agent
  - `DELETE /agents/<id>/` - Delete agent

- **AssociateViewset** (ModelViewSet):
  - `GET /associates/` - List associates (with filtering & pagination)
  - `POST /associates/` - Create new associate
  - `GET /associates/<id>/` - Retrieve specific associate
  - `PUT /associates/<id>/` - Update associate
  - `PATCH /associates/<id>/` - Partial update associate
  - `DELETE /associates/<id>/` - Delete associate

**URL Configuration:**
```python
# urls.py
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('agents', views.AgentViewset, basename='agent')
router.register('associates', views.AssociateViewset, basename='associate')

urlpatterns = [
    path('', include(router.urls)),
    # ... other paths
]
```

**Implementation:**

**Manual ViewSet:**
```python
# views.py
class AgentViewset(viewsets.ViewSet):
    def list(self, request):
        queryset = Employee.objects.all()
        serializer = EmployeeSerializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request):
        many = isinstance(request.data, list)
        serializer = EmployeeSerializer(data=request.data, many=many)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
    def retrieve(self, request, pk=None):
        agent = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(agent)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def update(self, request, pk=None):
        agent = get_object_or_404(Employee, pk=pk)
        serializer = EmployeeSerializer(agent, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        agent = get_object_or_404(Employee, pk=pk)
        agent.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

**ModelViewSet (The Ultimate):**
```python
# views.py
class AssociateViewset(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['emp_name']
```

---

### 6. Advanced Features - Blog API with Filtering & Pagination
**Endpoints**: 
- `GET/POST /blogs/` - Blog list with search, ordering, and pagination
- `GET/POST /comments/` - Comments list and creation
- `GET/PUT/PATCH/DELETE /blogs/<int:pk>/` - Individual blog operations
- `GET/PUT/PATCH/DELETE /comments/<int:pk>/` - Individual comment operations

**URL Configuration:**
```python
# urls.py
urlpatterns = [
    path('blogs/', views.BlogsView.as_view()),
    path('comments/', views.CommentsView.as_view()),
    path('blogs/<int:pk>/', views.BlogDetailView.as_view()),
    path('comments/<int:pk>/', views.CommentDetailView.as_view()),
]
```

**Models with Relationships:**
```python
# blogs/models.py
class Blog(models.Model):
    blog_title = models.CharField(max_length=100)
    blog_body = models.TextField()

    def __str__(self):
        return self.blog_title

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()

    def __str__(self):
        return self.comment
```

**Serializers with Nested Relationships:**
```python
# blogs/serializers.py
class CommentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class BlogSerializers(serializers.ModelSerializer):
    comments = CommentSerializers(many=True, read_only=True)  # Nested serialization
    class Meta:
        model = Blog
        fields = '__all__'
```

**Advanced Views Implementation:**
```python
# views.py
class BlogsView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializers
    pagination_class = LimitOffsetPagination
    # filter_backends = [DjangoFilterBackend]
    # filterset_class = BlogFilter
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['blog_body'] # Full-text search in blog content
    ordering_fields = ['id']      # Allow ordering by ID

class CommentsView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers

class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializers
    lookup_field = 'pk'

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    lookup_field = 'pk'
```

**Custom Filter Implementation:**
```python
# blogs/filters.py
import django_filters
from .models import Blog

class BlogFilter(django_filters.FilterSet):
    blog_title = django_filters.CharFilter(field_name='blog_title', lookup_expr='iexact')
    blog_body = django_filters.CharFilter(field_name='blog_body', lookup_expr='icontains')

    class Meta:
        model = Blog
        fields = ['blog_title', 'blog_body']
```

**Custom Pagination:**
```python
# api/paginations.py
class CustomPagination(PageNumberPagination, LimitOffsetPagination):
    page_size_query_param = 'page_size'
    page_query_param = 'page_num'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'results': data
        })
```

**Key Learning**:
- **Model Relationships**: Foreign keys and related field handling
- **Nested Serialization**: Including related objects in API responses
- **Search Functionality**: Full-text search across model fields
- **Ordering**: Dynamic result ordering based on client requests
- **Pagination**: Custom pagination with flexible parameters
- **Filter Backends**: Multiple filtering strategies in one view
- **Advanced Querying**: Complex database queries through DRF filters

**Example API Usage:**
```bash
# Search blogs containing "django"
GET /blogs/?search=django

# Order blogs by ID descending
GET /blogs/?ordering=id

# Paginate with custom page size
GET /blogs/?limit=5&offset=10

# Filter associates by name
GET /associates/?emp_name=John

# Get blog with all comments included
GET /blogs/1/  # Returns blog with nested comments array
```

## Advanced Features Implemented

### Custom Pagination
```python
class CustomPagination(PageNumberPagination, LimitOffsetPagination):
    page_size_query_param = 'page_size'
    page_query_param = 'page_num'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'count': self.page.paginator.count,
            'page_size': self.page_size,
            'results': data
        })
```

### Filtering & Search
- **DjangoFilterBackend**: Field-based filtering
- **SearchFilter**: Full-text search capabilities
- **OrderingFilter**: Dynamic result ordering
- **Custom FilterSets**: Advanced filtering logic

### Serializer Relationships
```python
class BlogSerializers(serializers.ModelSerializer):
    comments = CommentSerializers(many=True, read_only=True)
```

## Project Structure

```
django_rest_main/
├── api/                    # Main API application
│   ├── views.py           # All API view implementations
│   ├── serializers.py     # Data serialization logic
│   ├── urls.py            # URL routing
│   └── paginations.py     # Custom pagination classes
├── blogs/                 # Blog application
│   ├── models.py          # Blog and Comment models
│   ├── serializers.py     # Blog-specific serializers
│   └── filters.py         # Custom filter classes
├── employees/             # Employee application
└── students/              # Student application
```

## Key Learning Outcomes

### 1. **API Design Patterns**
- Understood the evolution from FBV to CBV to ViewSets
- Learnt when to use each pattern based on requirements
- Mastered REST API principles and HTTP method handling

### 2. **Django REST Framework Architecture**
- **Serializers**: Data validation and transformation
- **ViewSets & Routers**: Automatic URL generation and RESTful patterns
- **Mixins & Generics**: Code reusability and DRY principles

### 3. **Advanced Features**
- **Pagination**: Custom pagination for large datasets
- **Filtering**: Multiple filtering strategies (field-based, search, ordering)
- **Relationships**: Handling foreign key relationships in APIs

### 4. **Code Organization**
- Proper separation of concerns across apps
- Custom utility classes (pagination, filters)
- Scalable project structure

## API Endpoints Summary

| Endpoint | Pattern | Features |
|----------|---------|----------|
| `/students/` | Function-based | Basic CRUD |
| `/employees/` | Class-based Views | Manual HTTP methods |
| `/staffs/` | Mixins | Reusable components |
| `/workers/` | Generic Views | Minimal code |
| `/agents/` | ViewSet | Custom actions |
| `/associates/` | ModelViewSet | Full CRUD + Filtering |
| `/blogs/` | Generic + Advanced | Search, Ordering, Pagination |

## Technical Skills Demonstrated

 **Django REST Framework (DRF)**: Built robust RESTful APIs leveraging DRF's layered architecture including serializers, views, routers, and pagination.
* **Function-Based Views (FBVs)**: Implemented simple API endpoints using `@api_view`, ideal for lightweight operations and full control over request handling. Demonstrated clear separation of logic for different HTTP methods in views like `studentsView()` and `studentDetailView()`.
* **Class-Based Views (CBVs)**: Utilized DRF's class-based views such as `APIView`, generic views, and viewsets to build scalable and reusable endpoints.
* **APIView**: Used `APIView` to create more flexible endpoints that require custom logic while still benefiting from DRF's features like request parsing and standard responses (e.g., `Employees`, `EmployeeDetail` views).
* **Mixins + GenericAPIView**: Applied DRF mixins (`ListModelMixin`, `CreateModelMixin`, etc.) with `GenericAPIView` to handle partial CRUD operations in a modular way (e.g., `Staffs`, `StaffDetails`).
* **Generic Views**: Leveraged `ListCreateAPIView` and `RetrieveUpdateDestroyAPIView` to build efficient, DRY views with full CRUD support using minimal code (e.g., `BlogsView`, `CommentsView`, `WorkerDetails`).
* **ViewSets**: Created custom `ViewSet` classes to group related logic (list, retrieve, create, update, delete) and simplify routing using DRF's routers.
* **ModelViewSets**: Implemented `ModelViewSet` to automatically handle full CRUD for models like `Employee`, reducing boilerplate and enforcing REST principles.
* **Model Relationships**: Managed foreign key and reverse relationships between models (e.g., Blog ↔ Comment), with appropriate nested and related serializers.
* **Filtering, Searching, and Ordering**: Integrated `DjangoFilterBackend`, `SearchFilter`, and `OrderingFilter` to provide rich querying capabilities via query parameters.
* **Pagination**: Used `LimitOffsetPagination` and custom pagination classes to efficiently serve large datasets.
* **Error Handling**: Ensured consistent use of HTTP status codes, `Http404` exceptions, and DRF validation errors for reliable API responses.
* **Code Patterns Mastery**: Demonstrated deep understanding of multiple DRF patterns (FBVs, CBVs, mixins, generics, viewsets) and their ideal use cases in real-world API design.

---
