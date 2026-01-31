# Le Frat — Burger Store & Merchandise

🔗 **Live Site:**  
https://le-frat-store-9249b463cfe0.herokuapp.com/

🔗 **GitHub Repository:**  
https://github.com/madlp24/stage-pass  

---

## 📌 Project Overview  

Le Frat is a full-stack Django e-commerce platform developed as part of **Code Institute Project 5**.  
The project represents a burger-inspired lifestyle brand that sells exclusive merchandise, allowing users to browse products, manage a shopping bag, complete secure Stripe payments, and leave product reviews.

This project demonstrates skills in **full-stack development, UX design, Agile methodology, secure payments, database architecture, SEO optimization, and deployment**.

---

## 🏪 Business Model  

Le Frat operates under a **B2C (Business-to-Consumer)** model.

The brand merges:
- Burger culture  
- Streetwear identity  
- Lifestyle branding  

### 💰 Revenue Streams  
- Online merchandise sales (hoodies, t-shirts, accessories)  
- Limited edition drops  
- Brand collaborations and partnerships  

### 🎯 Value Proposition  
Le Frat delivers **a lifestyle experience beyond food**, blending culture, exclusivity, and identity into a recognizable and scalable brand.

---

## 👥 Target Audience  

### 🎯 Primary Audience  
- Ages 16–35  
- Urban, trend-aware, socially active  
- Fans of streetwear and food culture  

### 🎯 Secondary Audience  
- Tourists  
- Casual shoppers  
- Brand collectors  

---

## 📣 Marketing Strategy  

### 📘 Facebook Business Page  
A Facebook Business Page supports brand awareness, marketing, and customer engagement.

🔗 https://www.facebook.com/profile.php?id=61587399382148  

📸 **Evidence to include:**  
- Profile page screenshot  
- About section screenshot  
- Example promotional post  

---

### 📧 Email Marketing  
Users can subscribe to a **newsletter** to receive:
- Promotions  
- New product announcements  
- Limited edition releases  

This supports **customer retention and remarketing**.

---

### 🔍 SEO Strategy  
SEO practices implemented:
- `robots.txt`  
- `sitemap.xml`  
- SEO-friendly URLs  
- Optimized page metadata  
- Semantic HTML structure  
- Accessible UI components  

📸 **Evidence to include:**  
- Sitemap validation screenshot  
- Robots.txt screenshot  
- Meta tag inspection  

---

## 🎨 User Experience (UX) & Design  

### 🎯 UX Goals  
- Provide a clean and intuitive shopping experience  
- Enable fast and secure checkout  
- Encourage engagement through reviews  
- Maintain strong lifestyle brand identity  
- Optimize usability across mobile and desktop  

### 🎨 Design Choices  
- Minimalist layout  
- Brand-aligned typography and color palette  
- Mobile-first responsive design  
- Clear product hierarchy  
- Accessible navigation  

📸 *(Insert UI & responsive design screenshots here)*  

---

## 🗂️ Agile Development & Planning  

The project followed **Agile methodology**, with features built incrementally and tracked via a Kanban board.

### 📝 Example User Stories  
- As a customer, I want to browse products easily  
- As a user, I want to securely checkout  
- As a user, I want to leave reviews  
- As an admin, I want to manage inventory  
- As a customer, I want to subscribe to a newsletter  

📸 *(Insert screenshot of GitHub Projects / Kanban board here)*  

---

## ⚙️ Key Features  


### 📰 Newsletter Signup Form  

A newsletter signup form is implemented to support email marketing and customer retention.  
Users can subscribe to receive promotions, updates, and new product announcements.

📸 *(Insert newsletter signup UI screenshot here)*  

---

### 🚫 Custom 404 Page  

A custom **404 error page** has been created to improve user experience and maintain consistent branding when users navigate to invalid URLs.

📸 *(Insert custom 404 page screenshot here)*  

---

### 🧩 Proof of 3+ Custom Models  

The project includes **multiple original custom Django models**, designed to extend core functionality.

#### 🛍️ Product Model  
Stores product details including:
- Name  
- Description  
- Price  
- Stock  
- Image  

#### 📦 Order Model  
Handles checkout and order tracking:
- Customer information  
- Order totals  
- Stripe payment references  
- Order status  

#### ⭐ ProductReview Model  
Allows users to:
- Leave a rating (1–5)  
- Write a review  
- Upload an optional image  
- Edit or delete their own review  

#### 📧 NewsletterSubscription Model  
Stores newsletter subscribers:
- Email addresses  
- Subscription date  

These models demonstrate **custom database design**, **relational data structure**, and **full-stack CRUD functionality**, satisfying Code Institute requirements.

📸 *(Insert admin panel / database model screenshots here)*  

### 👤 User Accounts  
- User registration  
- Login / logout  
- Profile management  

---

### 🛍️ Product Management  
- Browse products  
- View product detail pages  
- Admin CRUD functionality  

---

### 🛒 Shopping Bag  
- Add products to bag  
- Update quantities  
- Remove products  

---

### 💳 Secure Checkout & Stripe Payments  
- Stripe payment integration  
- Stripe Webhooks  
- Secure order processing  
- Payment success and failure handling  
- Protection against duplicate orders  

📸 *(Insert Stripe webhook and checkout success screenshots)*  

---

### ⭐ Product Reviews System  
Users can:
- Leave **one review per product**  
- Rate products from **1–5**  
- Upload an optional image  
- Edit or delete their own reviews  

#### 📈 Business Value  
- Builds customer trust  
- Improves conversion rates  
- Encourages community engagement  
- Strengthens brand credibility  

📸 *(Insert review UI screenshots)*  

---

## 🗄️ Database Schema  

Core models:
- Product  
- Order  
- UserProfile  
- ProductReview  
- NewsletterSubscription  

📸 *(Insert ERD diagram screenshot here)*  

## 📊 ERD / Database Diagram  

The project includes a database schema designed to support e-commerce functionality, user accounts, orders, reviews, and newsletter subscriptions.

A simple ERD (Entity Relationship Diagram) was created to visually represent relationships between models.

📸 *(Insert ERD / database diagram screenshot here)*  

---

## 🧰 Technologies Used  

### 🎨 Frontend  
- HTML5  
- CSS3  
- Bootstrap  
- JavaScript  

### 🧠 Backend  
- Python  
- Django  

### 🗃️ Database  
- PostgreSQL  

### 💳 Payments  
- Stripe API  
- Stripe Webhooks  

### 🚀 Deployment  
- Heroku  
- Gunicorn  
- Whitenoise  

---

## 🧪 Testing  

### ✅ Manual Testing Summary  

| Feature | Action | Expected Result | Outcome |
|--------|--------|----------------|--------|
| User Registration | Create account | Account created | Pass |
| Login | Login with valid credentials | User logged in | Pass |
| Add to Bag | Add product | Product added | Pass |
| Update Bag | Change quantity | Bag updates correctly | Pass |
| Checkout | Complete payment | Order processed | Pass |
| Stripe Webhooks | Confirm payment | Payment validated | Pass |
| Reviews | Submit review | Review saved | Pass |
| Edit Review | Update review | Changes saved | Pass |
| Delete Review | Remove review | Review deleted | Pass |
| Admin CRUD | Manage products | Updates successful | Pass |
| Responsive Layout | Resize screen | Layout adapts | Pass |

All features were tested across **desktop and mobile devices**.

📸 *(Insert testing evidence screenshots if desired)*  

---

## 🚀 Deployment  

### 📦 Steps to Deploy on Heroku  

1. Install dependencies  
   ```bash
   pip install -r requirements.txt
### 2. Set environment variables  

- SECRET_KEY  
- DATABASE_URL  
- STRIPE_PUBLIC_KEY  
- STRIPE_SECRET_KEY  
- STRIPE_WEBHOOK_SECRET  

---

### 3. Run migrations  
    ```bash
python manage.py migrate
```
### 4. Collect static files  

```bash
python manage.py collectstatic
```
### 5. Deploy to Heroku  

*(Insert Heroku deployment proof screenshot)*  

---

## 🔐 Security  

- Sensitive credentials stored in environment variables  
- DEBUG disabled in production  
- CSRF protection enabled  
- Secure Stripe payment handling  
- Safe user authentication practices  

---

## ⚡ Performance & Lighthouse  

The site was tested using **Google Lighthouse** to measure:
- Performance  
- Accessibility  
- Best Practices  
- SEO  

📸 *(Insert Lighthouse results screenshot)*  

---

## 📸 Screenshots  

📌 **Suggested screenshots to include:**
- Homepage  
- Product listing  
- Product detail page  
- Shopping bag  
- Checkout success  
- Reviews section  
- Admin dashboard  
- Facebook Business Page  
- SEO validation  
- Deployment confirmation  

---

## 👤 Author  

**Le Frat — Code Institute Project 5**  

---

## 🙌 Acknowledgements  

Thanks to:
- Code Institute  
- My mentor  
- CI Student Community  
- Django & Stripe Documentation  

