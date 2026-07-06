# ⚡ QUICK REFERENCE CARD

## 📦 Your New Application

**Location**: `C:\Project\india-climate-portal-new\`

**Status**: ✅ Complete & Ready to Deploy

---

## 🚀 Deploy in 3 Steps

### To Streamlit Cloud:
```
1. Upload folder to GitHub
2. Go to share.streamlit.io
3. Deploy → Main file: app.py
```

### To Hugging Face:
```
1. Create Space (select Streamlit SDK)
2. Upload all 7 files
3. Wait 2 minutes → Done!
```

### Test Locally:
```bash
cd C:\Project\india-climate-portal-new
pip install -r requirements.txt
streamlit run app.py
```

---

## 📁 Files Overview

| File | Purpose | Size |
|------|---------|------|
| `app.py` | Main application | ~20 KB |
| `requirements.txt` | Dependencies (4 packages) | 32 bytes |
| `README.md` | Documentation | ~5 KB |
| `DEPLOY.md` | Deployment guide | ~6 KB |
| `.gitignore` | Git ignore | 272 bytes |
| `packages.txt` | System deps (none) | 55 bytes |
| `START_HERE.txt` | Quick start | ~6 KB |

**Total**: 7 files, ~37 KB

---

## ✨ Features

- ✅ 22+ Indian States
- ✅ 3 Climate Hazards (Cyclones, Floods, Droughts)
- ✅ 3 Scenarios (RCP 2.6, 4.5, 8.5)
- ✅ Value at Risk calculations
- ✅ Interactive maps
- ✅ Real CLIMADA data via API
- ✅ Download reports (CSV)

---

## 🎯 Why This Works

**vs. Original App**:
- ❌ No GDAL errors
- ❌ No dependency hell
- ✅ Uses API instead
- ✅ Deploys in 2 minutes
- ✅ Zero conflicts

**vs. Sample Data App**:
- ✅ Real CLIMADA data (not samples)
- ✅ Scientific credibility
- ✅ Actual climate datasets

---

## 📊 Technical Specs

**Dependencies**: Only 4!
```
streamlit
pandas
numpy
requests
```

**System Packages**: None!

**Python Version**: 3.8+

**API**: CLIMADA Data API (public, no key)

---

## 🔗 Quick Links

- **App Code**: `app.py`
- **Full Guide**: `DEPLOY.md`
- **Documentation**: `README.md`
- **Start Here**: `START_HERE.txt`

---

## ⚡ One-Minute Deploy

**Fastest**: Upload to Hugging Face Space

1. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
2. Name: `india-climate-portal`
3. SDK: **Streamlit**
4. Upload all 7 files
5. **Done!** ✅

URL: `https://huggingface.co/spaces/YOUR_USERNAME/india-climate-portal`

---

## 🎨 Customization

**Change title**: Line 11 of `app.py`

**Add states**: Line 24-45 (`INDIAN_STATES` dict)

**Modify colors**: Line 168-183 (CSS)

**Add logo**: Line 208 (sidebar image)

---

## 🐛 Troubleshooting

**Build fails**:
- Check Python version (use 3.10)
- Verify `requirements.txt` format
- Ensure SDK = Streamlit (if HF)

**App slow**:
- First load takes 2-3 min (normal)
- Cache warms up after first use
- Try smaller states first

**API errors**:
- Check internet connection
- CLIMADA API might be down (rare)
- Try again in 5 minutes

---

## ✅ Success Checklist

Deployment successful if:

- [ ] App loads without errors
- [ ] Can select state from dropdown
- [ ] "Run Analysis" button works
- [ ] CLIMADA data appears
- [ ] Maps display correctly
- [ ] VaR calculations complete
- [ ] Can download CSV

---

## 📞 Support

- **Deployment**: See `DEPLOY.md`
- **Features**: See `README.md`
- **Code**: Comments in `app.py`

---

## 🎉 You're Ready!

All files are complete. Just deploy!

**Next**: Read `DEPLOY.md` for your chosen platform

---

**Built for**: Climate risk assessment in India
**Powered by**: CLIMADA API + Streamlit
**Deploy to**: Streamlit Cloud / Hugging Face / Local

**Status**: 🟢 Production Ready
