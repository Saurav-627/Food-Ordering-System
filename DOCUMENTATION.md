# Khaja Kham - Comprehensive Technical Masterfile

## 1. System Architecture & Model Analysis
The Khaja Kham project is architected using a decoupled application strategy (Core, Foods, Orders, Users, Recommendations). Below is the granular analysis of the schema.

### 1.1 Model Granularity
| Entity | Logic & Neglected Parts | Scalability Factor |
| :--- | :--- | :--- |
| **User (Custom)** | Distinguishes between 3 roles. **Neglected Part**: Includes `address` and `phone` which are critical for Rider navigation but often missed in basic auth systems. | Can be extended for Merchant roles. |
| **Order** | Handles geospatial data (`lat`, `lng`) and a `delivery_boy` FK. **Neglected Part**: Specifically tracks `total_price` as a static field to prevent data drift. Now includes `payment_method` (COD, eSewa, Khalti) and `payment_status` for financial reconciliation. | Ready for GIS analysis and payment gateway integration. |
| **OrderItem** | **Neglected Part**: Uses `price_at_order`. This is a professional business requirement to ensure historical receipts remain accurate even if the menu price is updated. | Supports financial auditing. |
| **Food & Category** | Uses `slug` for SEO-friendly URLs. Includes `prep_time_min` for delivery window estimation. | Ready for multi-branch scaling. |

---

## 2. Advanced Mermaid ERD (Technical Level)
This diagram includes every field, relationship type, and key constraint.

```mermaid
erDiagram
    %% User & Auth
    USER {
        int id PK
        string username "Unique"
        string password
        string role "USER, DELIVERY_BOY, ADMIN"
        string phone
        text address
        datetime date_joined
    }

    %% Catalog
    CATEGORY {
        int id PK
        string name
        string slug "Unique/SEO"
        text description
    }

    FOOD {
        int id PK
        int category_id FK
        string name
        string slug "Unique/SEO"
        text description
        decimal price
        string image
        boolean is_available
        int prep_time_min
        datetime created_at
    }

    %% Transactions
    CART {
        int id PK
        int user_id FK "Null for sessions"
        string session_key "Unique for guests"
        datetime created_at
        datetime updated_at
    }

    CART_ITEM {
        int id PK
        int cart_id FK
        int food_id FK
        int quantity
    }

    ORDER {
        int id PK
        int user_id FK "Customer ID"
        int delivery_boy_id FK "Rider ID (Assigned)"
        string status "Enum: PENDING..COMPLETED"
        string payment_method "Enum: COD, ESEWA, KHALTI"
        string payment_status "Enum: PENDING, PAID, FAILED"
        decimal total_price "Locked at Checkout"
        text delivery_address
        float lat "Geo Data"
        float lng "Geo Data"
        datetime created_at
    }

    ORDER_ITEM {
        int id PK
        int order_id FK
        int food_id FK
        int quantity
        decimal price_at_order "Historical Snapshot"
    }

    %% Intelligence
    RATING {
        int id PK
        int user_id FK
        int food_id FK
        int rating "1-5 Scale"
        text review
    }

    RECOMMENDATION_CACHE {
        int id PK
        string key "Matrix Identifier"
        json data "Compressed Matrix"
        datetime updated_at
    }

    %% Relationships
    USER ||--o| CART : "manages"
    CART ||--|{ CART_ITEM : "holds"
    FOOD ||--o{ CART_ITEM : "indexed_in"
    USER ||--o{ ORDER : "purchases"
    USER ||--o{ ORDER : "fulfills"
    ORDER ||--|{ ORDER_ITEM : "contains"
    FOOD ||--o| ORDER_ITEM : "referenced_in"
    CATEGORY ||--o{ FOOD : "categorizes"
    USER ||--o{ RATING : "votes"
    FOOD ||--o{ RATING : "valued_by"
```

---

## 3. Dynamic Workflow Diagrams

### 3.1 Data Flow Diagram (DFD) - Level 1
This shows how data moves between storage layers and user interfaces.

```mermaid
graph TD
    subgraph Frontend
        A[Client Browser]
    end

    subgraph Logic_Layer
        B[Django Views]
        C[Recommendation Engine]
        D[Mapping Service]
    end

    subgraph Data_Store
        E[(PostgreSQL/SQLite)]
        F[(JSON Matrix Cache)]
    end

    A -->|POST: Order/Rating| B
    B -->|Query/Update| E
    E -->|Raw Data| C
    C -->|Update Matrix| F
    F -->|Top Recommendations| B
    B -->|Render Template| A
    D -->|Get GeoCoord| A
```

### 3.2 Order Lifecycle (Activity Diagram)
A high-resolution view of the state transitions.

```mermaid
stateDiagram-v2
    [*] --> PENDING: Order Placed
    PENDING --> ACCEPTED: Rider Accepts Job
    ACCEPTED --> ON_THE_WAY: Food Picked Up
    ON_THE_WAY --> COMPLETED: Signature/Delivery
    COMPLETED --> [*]: Transaction Closed
    
    PENDING --> CANCELLED: Out of Stock/User Cancel
    CANCELLED --> [*]
```

### 3.3 Sequence Diagram (The Logic Flow)
How the "People also ordered" logic actually triggers.

```mermaid
sequenceDiagram
    participant U as User
    participant V as View
    participant M as Model
    participant R as Recommendation Script

    U->>V: Completes Order
    V->>M: Create OrderItem
    V->>R: Trigger "train_co_occurrence()"
    R->>M: Query all COMPLETED orders
    M->>R: Returns list of items per order
    R->>R: Increment weights for Item Pairs
    R->>M: Save new weights to RecommendationCache
    V->>U: Show Success & "You might also like..."
```

---

## 4. Algorithmic Purpose & Definitions
1.  **Collaborative Filtering**: Used for **Personalization**. It solves the "Discovery Problem" - helping users find new food they didn't know they wanted.
2.  **Breadth-First Geolocation**: Used for **Logistics**. By mapping coordinates directly to the Rider dashboard, we solve the "Last-Mile Delivery" problem common in local food delivery.
3.  **Atomic Pricing**: By taking a snapshot (`price_at_order`), we solve the **Financial Drift** problem, ensuring business reports always match what the customer paid.
