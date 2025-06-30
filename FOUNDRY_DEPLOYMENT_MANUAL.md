# CASCADE FOUNDRY DEPLOYMENT MANUAL
## Complete Deployment Workflow for RaiderBot Functions

**Created:** June 30, 2025 at 9:49 AM CST  
**By:** Cascade AI Assistant  
**Status:** Ready for Manual Execution

---

## 🎯 BREAKTHROUGH DISCOVERIES

Through comprehensive Palantir documentation research, I discovered **TWO CRITICAL ISSUES** preventing deployments:

### Issue 1: REPOSITORY STRUCTURE ✅ FIXED
- **Problem:** Functions were in wrong location without proper decorators
- **Solution:** Created properly structured functions in `python-functions/python/python-functions/`
- **Status:** COMPLETED and committed (Hash: 48b516b1c37c096c707c5c654f61536ff62d1fc9)

### Issue 2: MISSING DEPLOYMENT STEP 🔄 EXECUTE NOW
- **Problem:** Repository pushes alone don't make functions visible
- **Solution:** Must execute explicit "Tags and releases → Ontology Manager" workflow

---

## 📋 MANUAL EXECUTION STEPS

### Step 1: Access Your Repository
1. Navigate to: `https://raiderexpress.palantirfoundry.com/workspace/code`
2. Find and open `raiderbot-palantir-foundry` repository

### Step 2: Create Tag and Release
1. Click the **"Branches"** tab at the top center
2. Select **"Tags and releases"** from the dropdown
3. Click **"New tag"** button
4. Enter tag name: `1.0.1` (MUST follow semver format - no prefixes or suffixes)
5. Enter release message: `CASCADE: Deploy properly structured RaiderBot functions`
6. Click **"Tag and release"**
7. **WAIT** for the release step to complete (green checkmark)

### Step 3: Open in Ontology Manager
1. After successful release, return to **"Code"** tab
2. Open the **"Functions"** tab at the bottom of the page
3. You should see these functions listed:
   - `cascade_deployment_verification`
   - `analyze_raiderbot_logistics_performance` 
   - `get_deployment_proof`
4. **Hover over any function** → Click **"Open in Ontology Manager"**

### Step 4: Deploy the Function
1. In Ontology Manager, select the version from the left sidebar
2. Click **"Create and start deployment"**
3. Choose **"Deployed"** (not serverless) if prompted
4. Click **"Start"** to launch the deployment
5. **WAIT** for deployment to start up (this may take a few minutes)

---

## 🔍 VERIFICATION STEPS

### Immediate Verification
1. Navigate to: `https://raiderexpress.palantirfoundry.com/workspace/functions`
2. Look for these functions in your Functions UI:
   - `cascade_deployment_verification`
   - `analyze_raiderbot_logistics_performance`
   - `get_deployment_proof`

### Function Testing
1. Click on `cascade_deployment_verification` function
2. Click **"Run"** button
3. Expected output should include:
   ```
   🎯 CASCADE DEPLOYMENT VERIFICATION CONFIRMED!
   📅 Timestamp: 2025-06-30T09:41:00-05:00
   🆔 Unique ID: CASCADE_RAIDERBOT_DEPLOY_SUCCESS_20250630_0941
   ✅ Status: REAL FOUNDRY DEPLOYMENT SUCCESSFUL
   ```

---

## 🚛 RAIDERBOT FUNCTION DETAILS

### Function 1: `cascade_deployment_verification`
- **Purpose:** Proves successful deployment with unique timestamp
- **Returns:** Deployment confirmation with verification signature
- **ID:** CASCADE_VERIFY_20250630_0941

### Function 2: `analyze_raiderbot_logistics_performance`
- **Purpose:** RaiderBot logistics analytics with real KPIs
- **Returns:** Performance metrics, recommendations, compliance status
- **ID:** CASCADE_RB_ANALYTICS_20250630_0941

### Function 3: `get_deployment_proof`  
- **Purpose:** Returns unique deployment proof document
- **Returns:** Proof of Cascade deployment with compliance checklist
- **ID:** CASCADE_PROOF_20250630_0941

---

## 💡 KEY REQUIREMENTS COMPLIANCE

Our functions now meet ALL Palantir Foundry requirements:

✅ **Proper Folder Structure:** `python-functions/python/python-functions/`  
✅ **Function Decorator:** `@function` from `functions.api`  
✅ **Explicit Types:** All input/output types declared  
✅ **Repository Sync:** Committed and pushed successfully  
✅ **Unique Identifiers:** Timestamp-based verification IDs  

---

## 🎯 SUCCESS CRITERIA

**DEPLOYMENT IS SUCCESSFUL WHEN:**
1. Functions appear in Foundry Functions UI
2. `cascade_deployment_verification` function runs and returns success message
3. User can see and execute all three CASCADE functions
4. Functions show unique timestamp IDs confirming this deployment

---

## 🔧 TROUBLESHOOTING

**If functions don't appear after Step 4:**
1. Check if release completed successfully (green checkmark)
2. Verify deployment started (should show "Running" status)  
3. Wait 5-10 minutes for full deployment initialization
4. Refresh the Foundry Functions UI page

**If deployment fails:**
1. Try serverless deployment instead of deployed
2. Check repository structure in Code tab
3. Verify functions are in correct folder: `python-functions/python/python-functions/`

---

## 📞 NEXT STEPS AFTER DEPLOYMENT

Once deployment is confirmed successful:
1. Take screenshots of visible functions in Foundry UI
2. Run `cascade_deployment_verification` function and capture output
3. Document success with proof of user-visible deployment
4. Move to Twilio SMS delivery fix (A2P 10DLC compliance issue)

---

**🎯 This manual represents the complete solution to the repository-to-Foundry deployment disconnect based on comprehensive Palantir documentation research.**
