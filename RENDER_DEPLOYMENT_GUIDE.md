# Render Deployment Troubleshooting Guide

## Current Status
- ✅ Local: Working perfectly
- ❌ Render: Not working

## Common Issues & Solutions

### Issue 1: OPENAI_API_KEY Not Set
**Symptom:** Recommendations show "Unable to analyze risk" or "Unable to generate recommendations"

**Solution:**
1. Go to Render Dashboard: https://dashboard.render.com
2. Find your service: `ai-compliance-assistant-0728`
3. Click "Settings"
4. Scroll to "Environment"
5. Add new variable:
   ```
   Key: OPENAI_API_KEY
   Value: sk-proj-xxxxx (your actual key)
   ```
6. Click "Save Changes"
7. Service will auto-restart

### Issue 2: PDFs Not Found on Render
**Symptom:** "Vectorstore not initialized" error

**Solution:**
The multi-path detection should handle this, but verify:
- PDFs are in `data/` folder locally ✅ (already fixed in code)
- Check Render logs for PDF loading messages

**Check Logs:**
```
Render Dashboard > Service > Logs
Look for: "Successfully loaded X PDF(s)"
```

### Issue 3: Frontend Not Loading
**Symptom:** Blank page or CSS/JS errors

**Solution:**
1. Check browser console (F12 > Console tab)
2. Look for CORS errors
3. Verify API URL in frontend is correct

**Frontend Fix (already applied):**
```javascript
const API_BASE_URL = window.location.origin;
// This automatically uses Render URL
```

### Issue 4: Backend API Not Responding
**Symptom:** Network error when clicking "Analyze Compliance"

**Check:**
1. Go to: `https://your-render-url/health`
2. Should return:
   ```json
   {
     "status": "ok",
     "vectorstore_ready": true,
     "message": "Vectorstore ready and documents loaded"
   }
   ```

### Issue 5: Slow Response Time
**Symptom:** Takes 30+ seconds to analyze

**This is normal!** OpenAI API takes 10-15 seconds per request (2 requests = 20-30 seconds)

---

## Step-by-Step Deployment Verification

### Step 1: Check Health Endpoint
```
URL: https://ai-compliance-assistant-0728.onrender.com/health
Expected: Status 200 with vectorstore_ready: true
```

### Step 2: Check Frontend Loads
```
URL: https://ai-compliance-assistant-0728.onrender.com/
Expected: Beautiful UI with all sections visible
```

### Step 3: Test API Directly
Use a REST client (Postman, Insomnia, or curl):
```bash
curl -X POST https://ai-compliance-assistant-0728.onrender.com/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the compliance requirements?"}'

Expected: JSON response with 3 sections
```

### Step 4: Check Browser Console
1. Open: https://ai-compliance-assistant-0728.onrender.com/
2. Press F12 (DevTools)
3. Click "Console" tab
4. Look for red errors
5. Common errors and fixes below

---

## Common Browser Console Errors

### Error: "Failed to fetch"
- **Cause:** Backend not responding or CORS issue
- **Fix:** Check if `/health` endpoint works in new tab

### Error: "API returned 500"
- **Cause:** Server error, usually missing OPENAI_API_KEY
- **Fix:** Set environment variable in Render

### Error: "Cannot read property 'retrieved_context'"
- **Cause:** API response format issue
- **Fix:** Likely OPENAI_API_KEY not set, causing error responses

---

## Environment Variables Checklist

On Render, you MUST have:
- ✅ `OPENAI_API_KEY` = sk-proj-xxxxx

Optional but recommended:
- `PYTHONUNBUFFERED=1` (for better logging)

---

## View Render Logs

1. Render Dashboard > Your Service
2. Click "Logs" tab
3. Look for:
   - `Application startup complete` ✅ (good)
   - `ERROR` messages (bad)
   - PDF loading messages

---

## Reset & Redeploy

If nothing works:

1. **Force Redeploy:**
   - Render Dashboard > Service > Manual Deploy > Latest

2. **Check Environment:**
   - Render Dashboard > Service > Settings > Environment
   - Verify OPENAI_API_KEY is set correctly

3. **Check Build Logs:**
   - Render Dashboard > Service > Build Logs tab
   - Look for install/build errors

---

## If Still Not Working

1. **Collect Information:**
   - Screenshot of error
   - Browser console errors (F12)
   - Render logs output
   - Health endpoint response

2. **Common Fixes:**
   - Clear browser cache (Ctrl+Shift+Del)
   - Try incognito/private window
   - Try different browser
   - Restart Render service

3. **Last Resort:**
   - Delete Render service
   - Redeploy from scratch
   - Ensure all env vars set BEFORE first deploy

---

## Service URLs

- **Frontend:** https://ai-compliance-assistant-0728.onrender.com/
- **Health Check:** https://ai-compliance-assistant-0728.onrender.com/health
- **API Endpoint:** https://ai-compliance-assistant-0728.onrender.com/analyze (POST only)

---

## Expected Response Format

**Successful analysis response:**
```json
{
  "retrieved_context": "Document excerpt...",
  "risk_analysis": "Compliance risk assessment...",
  "pm_output": "1. Recommendation 1\n2. Recommendation 2\n..."
}
```

**Error response:**
```json
{
  "error": "Vector store not initialized",
  "details": "PDFs not loaded on startup...",
  "retrieved_context": "ERROR: No documents available",
  "risk_analysis": "ERROR: Cannot analyze...",
  "pm_output": "ERROR: Please ensure PDF files..."
}
```

---

## Quick Checklist

Before declaring deployment successful:

- [ ] Frontend loads at https://ai-compliance-assistant-0728.onrender.com/
- [ ] Health endpoint returns status 200
- [ ] Vectorstore shows as ready
- [ ] Can enter a compliance question
- [ ] "Analyze Compliance" button is clickable
- [ ] Results display with all 3 sections
- [ ] Recommendations show as numbered list
- [ ] No red errors in browser console

If all checkboxes pass → ✅ **DEPLOYMENT SUCCESSFUL!**

---

## Support

If you encounter issues:
1. Check logs in Render Dashboard
2. Verify OPENAI_API_KEY is set
3. Try manual redeploy
4. Check browser console (F12)
5. Verify API directly with test request
