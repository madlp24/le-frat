# Le Frat Store

A Django e-commerce store for a burger-inspired streetwear brand. Customers browse a product catalog, build a session-based bag, and check out with Stripe; staff manage inventory through an admin UI and authenticated users can post and manage their own product reviews.

**Live site:** https://le-frat-store-9249b463cfe0.herokuapp.com/

---

## The Problem

Small independent apparel brands usually start on a general-purpose storefront like Shopify or Etsy, which is fine for listings but gives the brand little control over the checkout experience, media hosting, and trust signals like user-generated reviews. Self-hosting a full store is the alternative, but most starter templates either skip real payment integration, skip file hosting beyond the local filesystem, or skip the authorization rules needed to let users leave and manage reviews without stepping on each other.

## The Solution

Le Frat Store is a self-hosted Django storefront that covers the full purchase path: catalog → session bag → Stripe checkout → persisted order → user-owned reviews. Media and static assets are served from S3 in production via a small custom storage backend, payments are verified server-side against the Stripe API before orders are saved, and reviews are scoped to their author so one user cannot edit or delete another user's content.

---

## Features

- **Product catalog** with full-text search over name/description, category filter, and sort by price, name, or newest (`products/views.py:product_list`).
- **Dynamic listing heading** that reflects the current context — Shop, New Arrivals, category name, or Search Results — rather than a hardcoded label.
- **Staff-only product CRUD** gated by `@user_passes_test(is_admin)` on add/edit/delete views.
- **Session-based shopping bag** (`bag/`) with add, update-quantity, and remove endpoints; bag state survives page navigation without requiring a logged-in user.
- **Stripe Elements checkout** with a server-side-created PaymentIntent and Stripe Elements rendered on the front end (`checkout/views.py`, `checkout/templates/checkout/checkout.html`).
- **Server-side order verification** — on return from Stripe, the success view retrieves the PaymentIntent directly from Stripe's API and checks both `amount` and `status` before persisting the order.
- **S3-backed media and static storage** in production via a custom `S3Boto3Storage` subclass (`custom_storages.py`), toggled by the `USE_AWS` environment variable.
- **WhiteNoise compressed static files** for local/dev and for Heroku deployments that don't use S3.
- **User accounts via django-allauth** with email-or-username login and a customizable signup form.
- **Ownership-protected reviews** — `add_review`, `edit_review`, and `delete_review` enforce `review.user == request.user or request.user.is_staff` before mutating, so users can only manage their own reviews.
- **User profile page** with an order lookup by order number (`profiles/views.py`).
- **Newsletter signup** and static marketing pages (About, FAQs, Support, Privacy, Terms) under a dedicated app.
- **Sitemap** via `django.contrib.sitemaps` for search engine discovery.

---

## Tech Stack

| Layer | Choice |
|---|---|
| Language / runtime | Python (see `runtime.txt`) |
| Web framework | Django 6.0 |
| Authentication | django-allauth |
| Payments | Stripe (stripe Python SDK + Stripe Elements) |
| Database (prod) | PostgreSQL via `psycopg2-binary` + `dj-database-url` |
| Database (dev) | SQLite (Django default) |
| Object storage (prod) | AWS S3 via `boto3` + `django-storages` |
| Static files (no-S3) | WhiteNoise |
| Application server | Gunicorn |
| Image handling | Pillow |
| Env var loading | python-dotenv |

---

## Architecture

The project is split into seven Django apps, each with a narrow responsibility:

- **`home/`** — landing page and root-level views.
- **`products/`** — `Product` and `Category` models, the catalog listing with search/filter/sort, product detail page (which also renders the reviews list and review form), and staff-only CRUD.
- **`bag/`** — session-backed shopping bag. No model — bag contents live in `request.session`. Exposes `add`, `update`, `remove`, and `view` endpoints, and publishes a context processor so the bag total is available in any template.
- **`checkout/`** — `Order` and `OrderLineItem` models, the Stripe Elements checkout page, the success view that re-verifies the PaymentIntent server-side, and the order admin.
- **`profiles/`** — user profile page and order detail lookup; uses a `post_save` signal (`profiles/signals.py`) to create a profile when a new `User` is created.
- **`marketing/`** — newsletter signup form plus static content pages (About, FAQs, Support, Privacy, Terms).
- **`reviews/`** — `ProductReview` model and the add/edit/delete views, with ownership checks on mutation. Reviews are rendered inline on the product detail page rather than on their own listing page.

The project settings and root URL conf live in `lefrat/`, and `custom_storages.py` at the repo root provides the two S3 storage subclasses.

---

## Key Technical Decisions

### 1. Server-side PaymentIntent re-verification over webhooks

After the Stripe Elements confirmation completes, the browser is redirected to the success view with the PaymentIntent ID in the query string. Rather than trusting the redirect alone, the success view calls `stripe.PaymentIntent.retrieve(payment_intent_id)` and checks that the returned `amount` matches the server-computed grand total (in cents) and that the intent's `status` is `succeeded` before saving the `Order` (`checkout/views.py`). This keeps the flow simple and avoids the webhook endpoint, signature verification, and deployment-environment configuration that webhooks require.

The tradeoff is that order creation depends on the browser completing the redirect. If the user closes the tab between Stripe confirmation and the server return, the payment will have succeeded on Stripe's side but no `Order` row will be written. Webhook support is a planned improvement (see Future Improvements) to close this gap — the event `payment_intent.succeeded` would trigger order creation if it hasn't already happened.

### 2. Custom storage backend for media files

Django's default `FileSystemStorage` assumes a writable local filesystem, which doesn't survive on ephemeral hosts like Heroku dynos, and doesn't separate static assets from user-uploaded media. `custom_storages.py` defines two small `S3Boto3Storage` subclasses:

- `StaticStorage` writes to the `static/` prefix of the S3 bucket.
- `MediaStorage` writes to the `media/` prefix and, critically, sets `file_overwrite = False` so two users uploading files with the same name don't clobber each other's images.

These are wired into Django's `STORAGES` setting only when `USE_AWS=True`, so local development defaults to filesystem storage and WhiteNoise for statics without needing AWS credentials.

### 3. Ownership-protected reviews

The review app uses an explicit check at the top of `edit_review` and `delete_review`:

```python
if review.user != request.user and not request.user.is_staff:
    messages.error(request, "You can't edit someone else's review.")
    return redirect("product_detail", product_id=review.product_id)
```

This sits next to the mutation it guards, so it's hard to miss when someone modifies the view later. Users cannot bypass it by guessing `/reviews/<id>/edit/` URLs directly, because the check runs before any form handling. A staff bypass is included so moderators can remove abusive content without impersonating the reviewer.

---

## Local Setup

```bash
# 1. Clone and enter the repo
git clone <repo-url>
cd le-frat

# 2. Create and activate a virtualenv
python -m venv .venv
source .venv/bin/activate        # on Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file with the required variables (see below)

# 5. Apply migrations and create a superuser
python manage.py migrate
python manage.py createsuperuser

# 6. Run the dev server
python manage.py runserver
```

### Required environment variables

```
SECRET_KEY=<django secret key>
DEBUG=True                        # for local only
DATABASE_URL=<optional; omit to use SQLite>
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WH_SECRET=whsec_...        # reserved; not yet consumed (see Known Limitations)
USE_AWS=False                     # set to True in production with AWS keys below
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```

### Stripe CLI

The [Stripe CLI](https://stripe.com/docs/stripe-cli) is useful during local checkout testing:

```bash
stripe listen
```

This streams live test-mode events (e.g. `payment_intent.created`, `payment_intent.succeeded`) so you can watch what the checkout flow is doing. There is no webhook endpoint to forward events to yet — `stripe listen --forward-to <url>` will become useful once webhook handling is implemented (see Future Improvements).

---

## Testing

```bash
python manage.py test
```

**Current state:** the per-app `tests.py` files are empty Django boilerplate — there is no meaningful test coverage yet. Building out a real test suite is the top item under Future Improvements.

---

## Known Limitations

- **Payment confirmation relies on the post-checkout redirect succeeding.** Users who close the tab before the redirect completes may not have their order saved. Webhook support is planned to handle this edge case.
- **No test coverage.** The test suite is currently unpopulated; the codebase is manually verified only.
- **No email delivery in production.** The email backend is set to `console.EmailBackend`, so order confirmations and other transactional emails are logged rather than sent.
- **Account email verification is disabled** (`ACCOUNT_EMAIL_VERIFICATION = "none"`), meaning new signups can transact without confirming their address.

---

## Future Improvements

- Implement a Stripe webhook handler for `payment_intent.succeeded` to guarantee order creation even when the post-checkout redirect is dropped.
- Populate the test suite — model validation, session-bag behaviour, checkout amount-mismatch handling, review ownership enforcement, and access control on staff-only views.
- Swap the console email backend for a real transactional email provider and send order confirmations.
- Enable account email verification and a password-reset flow through allauth.
- Add CI (GitHub Actions) to run migrations and tests on every push.
- Extract the `Order` creation path into a service function shared between the success-view flow and the future webhook handler, so both code paths produce identical order rows.
