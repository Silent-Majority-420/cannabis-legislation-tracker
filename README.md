# Federal Cannabis Legislation Tracker

A real-time tracker for federal cannabis legislation with AI-powered analysis using the CBDT Framework.

## Features

- **Real-time Updates**: Automatically fetches the latest federal cannabis bills from LegiScan API
- **Smart Filtering**: Search and filter bills by status, keywords, and date
- **AI-Powered Analysis**: Links to in-depth CBDT Framework analysis for significant bills
- **Responsive Design**: Beautiful, modern interface that works on all devices
- **Open Source**: Free to use and modify

## Live Demo

Visit the tracker at: [Your GitHub Pages URL]

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- LegiScan API key ([Get one here](https://legiscan.com/legiscan))
- Git
- GitHub account

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/cannabis-legislation-tracker.git
   cd cannabis-legislation-tracker
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your LegiScan API key**
   ```bash
   export LEGISCAN_API_KEY="your_api_key_here"
   ```
   
   Or on Windows:
   ```cmd
   set LEGISCAN_API_KEY=your_api_key_here
   ```

4. **Run the scraper to fetch bills**
   ```bash
   python scraper.py
   ```
   
   This will create a `bills.json` file with the latest federal cannabis legislation.

5. **Test locally**
   
   Open `index.html` in your web browser or use a local server:
   ```bash
   python -m http.server 8000
   ```
   
   Then visit `http://localhost:8000` in your browser.

### Deploying to GitHub Pages

1. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/cannabis-legislation-tracker.git
   git branch -M main
   git push -u origin main
   ```

2. **Enable GitHub Pages**
   - Go to your repository settings
   - Navigate to "Pages" in the left sidebar
   - Under "Source", select "main" branch
   - Click "Save"
   - Your tracker will be live at `https://yourusername.github.io/cannabis-legislation-tracker/`

## Workflow: Adding Analysis to Bills

The tracker is designed to work seamlessly with your cannabis policy analysis workflow:

### 1. Update Bill Data

Run the scraper regularly to fetch new bills:
```bash
python scraper.py
```

### 2. Identify Significant Bills

Review `bills.json` to find bills worthy of in-depth analysis:
- Look for bills with major policy implications
- Consider bills with high potential for passage
- Identify bills that align with your CBDT Framework insights

### 3. Create Analysis Articles

For significant bills:
1. Write a comprehensive analysis article on silentmajority420.com
2. Apply the CBDT Framework to predict outcomes
3. Publish the article and note its URL

### 4. Link Analysis to Bills

Edit `bills.json` to add your analysis URL:
```json
{
  "bill_number": "H.R. 420",
  "title": "Cannabis Administration and Opportunity Act",
  "analysis_url": "https://silentmajority420.com/hr420-cbdt-analysis"
}
```

### 5. Update the Tracker

Commit and push the updated `bills.json`:
```bash
git add bills.json
git commit -m "Add analysis link for H.R. 420"
git push
```

GitHub Pages will automatically rebuild your site, and the "Read CBDT Analysis" button will appear for that bill.

## Automation Options

### GitHub Actions (Recommended)

Set up automatic updates using GitHub Actions:

1. Create `.github/workflows/update-bills.yml`:
   ```yaml
   name: Update Bills Data
   
   on:
     schedule:
       - cron: '0 0 * * *'  # Run daily at midnight
     workflow_dispatch:  # Allow manual trigger
   
   jobs:
     update:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v2
         
         - name: Set up Python
           uses: actions/setup-python@v2
           with:
             python-version: '3.9'
         
         - name: Install dependencies
           run: pip install -r requirements.txt
         
         - name: Run scraper
           env:
             LEGISCAN_API_KEY: ${{ secrets.LEGISCAN_API_KEY }}
           run: python scraper.py
         
         - name: Commit and push if changed
           run: |
             git config --global user.name 'GitHub Action'
             git config --global user.email 'action@github.com'
             git add bills.json
             git diff --quiet && git diff --staged --quiet || (git commit -m "Update bills data" && git push)
   ```

2. Add your LegiScan API key to GitHub Secrets:
   - Go to repository Settings > Secrets and variables > Actions
   - Add a new secret named `LEGISCAN_API_KEY` with your API key

### Manual Cron Job

Or set up a local cron job to run the scraper:

```bash
# Run scraper daily at 6 AM
0 6 * * * cd /path/to/cannabis-legislation-tracker && python scraper.py && git add bills.json && git commit -m "Update bills" && git push
```

## Project Structure

```
cannabis-legislation-tracker/
├── index.html          # Main HTML page
├── style.css          # Styling and layout
├── app.js             # Frontend JavaScript
├── scraper.py         # Python scraper for LegiScan API
├── bills.json         # Generated bill data
├── requirements.txt   # Python dependencies
├── README.md          # This file
└── LICENSE           # MIT License
```

## Customization

### Branding

Update the header and footer in `index.html` to match your brand:
- Change the site title
- Update links to your website
- Modify the color scheme in `style.css`

### Styling

The tracker uses CSS variables for easy theming. Edit these in `style.css`:

```css
:root {
    --primary-color: #2ecc71;  /* Main brand color */
    --secondary-color: #3498db; /* Secondary color */
    --accent-color: #e74c3c;   /* Accent color */
    /* ... more variables ... */
}
```

### Filters

Add or modify filters in `index.html` and `app.js` to suit your needs.

## API Rate Limits

LegiScan API has rate limits:
- Free tier: 30,000 requests per month
- This tracker typically uses ~5-10 requests per update

Run the scraper once daily to stay well within limits.

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Support

For questions or issues:
- Open an issue on GitHub
- Visit [silentmajority420.com](https://silentmajority420.com)
- Email: [your contact email]

## Acknowledgments

- LegiScan API for providing comprehensive legislative data
- The CBDT Framework for cannabis market analysis methodology
- The cannabis policy reform community

---

**Built by Silent Majority 420** | [Website](https://silentmajority420.com) | [CBDT Framework](https://silentmajority420.com/cbdt-framework)
