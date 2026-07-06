# 🚀 Deployment Guide

## ✅ Quick Deploy Options

Choose your preferred platform:

### Option 1: Streamlit Cloud (Easiest) ⭐
### Option 2: Hugging Face Spaces (Like the example)
### Option 3: Local Development

---

## 🎯 Option 1: Streamlit Cloud

**Time**: 5 minutes | **Cost**: FREE

### Steps:

1. **Push to GitHub**
   ```bash
   cd india-climate-portal-new
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR_USERNAME/india-climate-portal.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Main file: `app.py`
   - Click "Deploy"

3. **Done!**
   - Your app will be live at: `https://YOUR_APP.streamlit.app`

---

## 🎯 Option 2: Hugging Face Spaces

**Time**: 5 minutes | **Cost**: FREE

### Steps:

1. **Create a Space**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Name: `india-climate-risk-portal`
   - License: MIT
   - SDK: **Streamlit**
   - Click "Create Space"

2. **Upload Files**

   **Method A - Web Upload**:
   - Click "Files" tab
   - Click "Add file" → "Upload files"
   - Upload:
     - `app.py`
     - `requirements.txt`
     - `README.md`
     - `.gitignore`
     - `packages.txt`
   - Commit changes

   **Method B - Git Push**:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/india-climate-risk-portal
   cd india-climate-risk-portal
   cp /path/to/india-climate-portal-new/* .
   git add .
   git commit -m "Add climate risk portal"
   git push
   ```

3. **Configure (Optional)**
   - Go to "Settings" tab
   - Set Python version: 3.10
   - Set hardware: CPU (free)

4. **Done!**
   - Your app will be live at: `https://huggingface.co/spaces/YOUR_USERNAME/india-climate-risk-portal`

---

## 🎯 Option 3: Local Development

**Time**: 2 minutes

### Steps:

1. **Install Python** (3.8 or higher)
   - Download from [python.org](https://python.org)

2. **Install Dependencies**
   ```bash
   cd india-climate-portal-new
   pip install -r requirements.txt
   ```

3. **Run the App**
   ```bash
   streamlit run app.py
   ```

4. **Open Browser**
   - Automatically opens at: `http://localhost:8501`

---

## 📋 Pre-Deployment Checklist

Before deploying, ensure:

- [ ] All files are in the folder
- [ ] `app.py` exists and is the main file
- [ ] `requirements.txt` has all dependencies
- [ ] `README.md` is clear and informative
- [ ] `.gitignore` excludes unnecessary files
- [ ] No sensitive data or API keys in code

---

## 🔍 File Structure Check

Your folder should look like this:

```
india-climate-portal-new/
├── app.py                 ✅ Main application
├── requirements.txt       ✅ Dependencies
├── README.md             ✅ Documentation
├── .gitignore            ✅ Git ignore
├── packages.txt          ✅ System packages (empty)
└── DEPLOY.md             ✅ This file
```

---

## 🐛 Troubleshooting

### Streamlit Cloud Issues

**Problem**: App won't deploy
- Check logs in Streamlit Cloud dashboard
- Verify `requirements.txt` is correct
- Make sure repository is public

**Problem**: App crashes on startup
- Check Python version (use 3.10)
- Verify all imports in `app.py`
- Check for typos in file paths

### Hugging Face Issues

**Problem**: Build fails
- Check that SDK is set to "Streamlit"
- Verify `requirements.txt` format
- Check logs in Space settings

**Problem**: Slow loading
- First build takes 2-3 minutes (normal)
- Subsequent loads are cached and fast

### Local Issues

**Problem**: Module not found
```bash
pip install -r requirements.txt --force-reinstall
```

**Problem**: Streamlit not found
```bash
pip install streamlit --upgrade
```

---

## 🎨 Customization

### Change App Title
Edit line 11 in `app.py`:
```python
page_title="Your Custom Title",
```

### Add More States
Edit `INDIAN_STATES` dictionary in `app.py`:
```python
"Your State": {"lat": XX.XX, "lon": YY.YY, "pop": ZZZZZ, "area": AAAA},
```

### Modify Color Scheme
Edit CSS in lines 168-183 of `app.py`

### Add Your Logo
Replace placeholder image URL in sidebar (line 208)

---

## 📊 Performance Tips

### For Streamlit Cloud:
- Use caching: `@st.cache_data`
- Limit API calls
- Sample large datasets

### For Hugging Face:
- Enable cache persistence
- Use CPU tier (free)
- Optimize image sizes

---

## 🔐 Security Notes

- No API keys required (CLIMADA API is public)
- No user data stored
- All calculations client-side
- Safe for public deployment

---

## 📈 Monitoring

### Streamlit Cloud:
- Dashboard shows viewer count
- Access logs available
- Performance metrics
- Error tracking

### Hugging Face:
- View counter on Space page
- Activity logs
- Usage statistics

---

## 🆕 Updates

To update your deployed app:

**Streamlit Cloud**:
1. Push changes to GitHub
2. App auto-rebuilds

**Hugging Face**:
1. Upload new files or push to Git
2. Space auto-rebuilds

**Local**:
1. Pull latest code
2. Restart app

---

## ✅ Success Criteria

Your deployment is successful if:

1. ✅ App loads without errors
2. ✅ Can select a state
3. ✅ Can choose hazard and scenario
4. ✅ "Run Analysis" works
5. ✅ Results display correctly
6. ✅ CLIMADA API connection works
7. ✅ Maps render properly
8. ✅ VaR calculations complete

---

## 🎉 Next Steps

After successful deployment:

1. **Share** your app URL
2. **Gather** user feedback
3. **Iterate** and improve
4. **Monitor** usage and performance
5. **Update** with new features

---

## 📞 Getting Help

- **Streamlit**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **Hugging Face**: [discuss.huggingface.co](https://discuss.huggingface.co)
- **GitHub Issues**: Open an issue in your repo

---

**Happy Deploying!** 🚀

Your climate risk portal will help decision-makers understand and prepare for climate impacts!
