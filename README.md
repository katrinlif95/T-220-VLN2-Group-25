# ArtVault

ArtVault is a Django-based web application for browsing and bidding on artworks from artists and galleries.

---

## Built with

- Django
- Python
- HTML/CSS
- JavaScript
- PostgreSQL
- Microsoft Azure
- Git

---

## Getting started

### Prerequisites

Recommended software:

- Python 3.13
- Git  (only required for GitHub setup)
- Visual Studio Code or PyCharm (optional)

If you have to install Python, restart VS Code, PyCharm or the terminal before continuing.

Verify installation:

```bash
python --version
```

---

### Installation

#### Setup using ZIP file

1. Download and extract the ZIP file
2. Open the extracted project folder in VS Code or PyCharm
3. Open a terminal inside the project folder
4. Continue from “Create virtual environment” in the installation instructions

---

#### Setup using GitHub

##### 1. Clone the repository

```bash
git clone https://github.com/katrinlif95/T-220-VLN2-Group-25.git
cd T-220-VLN2-Group-25
```

---

##### 2. Create virtual environment

###### Windows

```bash
python -m venv .venv
```

###### Mac/Linux

```bash
python3 -m venv .venv
```

---

##### 3. Activate virtual environment

###### Windows (PowerShell)

```bash
.venv\Scripts\activate
```

###### Mac/Linux

```bash
source .venv/bin/activate
```

After activation, you should see:

```bash
(.venv)
```

in the terminal.

If an error occurs, see section "PowerShell Execution Policy Error".

---

##### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

##### 5. Create `.env` file

Create a file named `.env` in the root project folder
(the same folder as `manage.py`).

Add the database password provided in the Canvas submission comment:

```env
DB_PASSWORD=database_password
```

---

##### 6. Apply migrations

```bash
python manage.py migrate
```

---

##### 7. Run the development server

```bash
python manage.py runserver
```

Open in browser:

```text
http://127.0.0.1:8000/
```

---

## Usage

Once the server is running successfully, the ArtVault application should be accessible in the browser.

---

## Notes for grading

### Demo accounts

No predefined demo user accounts are included.  
Users may create accounts directly through the application.

---

### Seller functionality

Seller-side functionality for accepting bids was not implemented as a separate seller workflow.
For testing purposes, bid statuses can be changed through the Django admin panel.

To test the finalize payment process:

1. Create a bid (or bids) using a normal user account
2. Create a Django superuser:

```bash
python manage.py createsuperuser
```

3. Run the server and log in to the Django admin panel:

```text
http://127.0.0.1:8000/admin/
```

4. In the admin panel, go to **Bid → Bids**
5. Select the bid that should be accepted
6. Change the bid Status from Pending to Accepted or Contingent
7. Click Save
8. Log back in as the normal user
9. The user can now continue to the finalize payment process

---

### Test expired bids

To test the expired bid functionality without waiting for the original expiration date:

1. Log in to the Django admin panel:

```text
http://127.0.0.1:8000/admin/
```

2. Go to **Bid → Bids**
3. Select a bid
4. Under **Expires at**, change the expiration date/time to a near-future time (for example 1–2 minutes ahead)
5. Click Save
6. Refresh the page after the expiration time has passed
7. The bid status should automatically update to `Expired`.

---

## Additional features implemented

The following additional features and improvements were implemented beyond the core project requirements:

### UI & user experience

- Responsive design for different screen sizes and resolutions
- Breadcrumb navigation across multiple pages
- Hover effects and button animations
- Descriptive alt text added to artwork and UI images for improved accessibility

---

### Navigation & browsing

- Clicking “Explore” on the homepage displays artworks marked as “Highlights this week”
- View all galleries through the “Galleries” navigation tab
- View artists through the “Artists” navigation tab (just artists who are sellers)
- Artist and gallery pages have lists and links to seller profiles
- Footer navigation links and informational pages
- Ability to navigate between artworks directly from the artwork detail page
- “More by this artist” button instead of a “Submit a bid” button on sold artwork detail pages which links to a page with all artworks by the artist

---

### Artwork & filtering features

- Display “Current highest bid” on:
  - all artworks page
  - artwork detail pages
  - user bids page
- Sold artworks display the “Final bid” instead of “Current highest bid”
- Artwork filtering for status (available/sold)
- Expandable artwork search bar with enhanced UI/UX
- Interactive price range slider filter based on minimum and maximum artwork prices
- Ability to clear individual filters or all filters simultaneously

---

### Account & profile features

- Logged-out users see “Please log in or sign up to place a bid” with links instead of a “Submit a bid” button
- Under My Account → Profile, profile image is clickable for editing along with “Change profile image” option
- Unsaved changes info message on profile before user presses update
- Validation messages for invalid names or unsupported symbols
- Updating button state while profile information is being saved
- Saved contact information connected to the payment process so users can reuse saved contact information while still being able to edit it during checkout if needed
- Info message for logged-in users regarding unpaid and/or outbid bids

---

### Bid system features

- Validation errors when:
  - submitting bids lower than the current highest bid
  - selecting expired bid expiration dates
- Users can view their own bid amount along with bid status on artwork detail pages
- Bid filtering functionality on My Account → Bids
- Counters on bid filters showing the number of Pending, Outbid and Unpaid bids
- Automatic “Expired” status for bids past their expiration date
- “Outbid” label on bids where a user has been outbid by another user
- Bid list prioritized and ordered based on bid status and required user actions
- When a bid is accepted and paid for, all other pending bids on the same artwork are automatically rejected

---

### Payment & validation features

- Validation messages for all required payment fields
- Users cannot bypass payment step requirements through URL manipulation
- Payment step URLs remain inaccessible until required information has been completed
- Sticky order summary during payment process

---

## PowerShell execution policy error

If you get an error when activating the virtual environment:

```powershell
cannot be loaded because running scripts is disabled on this system
```

Run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating the virtual environment again:

```powershell
.venv\Scripts\activate
```
