# Testing Documentation

## Test Suite Overview

### 1. Logic Tests (`test_sequential.py`)

**Purpose**: Verify animation logic without requiring Blender installation.

**What it tests**:
- Element position preservation (X, Z should never change)
- Y-axis animation (only axis that should move)
- Position diversity (elements should be spread in space, not overlapping)
- Understanding of origin_set behavior

**Run**:
```bash
python test_sequential.py
```

**Expected output**: All tests pass ✅

---

## Manual Testing Checklist

Before pushing changes, verify:

### Syntax & Structure
- [ ] `python -m py_compile ALTER_LOGO_SEQUENTIAL.py` → No errors
- [ ] Script has valid Python syntax
- [ ] All functions are defined
- [ ] Main() function exists
- [ ] Imports are correct

### Logic Tests
- [ ] `python test_sequential.py` → All pass
- [ ] X coordinates stay constant during animation
- [ ] Z coordinates stay constant during animation
- [ ] Y coordinates animate correctly (offset then return)
- [ ] Elements are NOT all at same position

### Integration (Requires Blender)
- [ ] Script runs without errors: `blender --background --python ALTER_LOGO_SEQUENTIAL.py`
- [ ] alter_logo_sequential_FAST.blend is created
- [ ] File can be opened in Blender
- [ ] Elements visible in viewport
- [ ] Elements are properly positioned (not overlapping)
- [ ] Animation timeline shows movement
- [ ] Fire materials are present

### Visual Verification (In Blender)
- [ ] Open generated .blend file
- [ ] Press SPACEBAR → Animation plays
- [ ] Elements come one by one from back
- [ ] Elements stay in formation (proper layout)
- [ ] Elements DON'T overlap
- [ ] Fire visible in Rendered mode (Z → Rendered)
- [ ] BANJA LUKA text appears at end

---

## Test Results

### Last Run: 2025-11-13

| Test | Status | Notes |
|------|--------|-------|
| Python syntax | ✅ PASS | No syntax errors |
| AST parse | ✅ PASS | Valid structure, 9 functions |
| Logic tests | ✅ PASS | All animation logic correct |
| Position preservation | ✅ PASS | X,Z stay constant |
| Y-axis animation | ✅ PASS | Correct offset and return |
| Position diversity | ✅ PASS | Elements spread in space |

---

## Known Limitations

1. **Cannot fully test without Blender**: Some tests require actual Blender execution
2. **SVG dependency**: Tests assume valid alter.svg exists
3. **No render output verification**: Cannot verify final rendered frames without Blender

---

## Debug Tips

### Elements overlapping?
Check element positions after import:
```python
for i, elem in enumerate(elements):
    print(f"Element {i}: location = {elem.location}")
```
Expected: Different X,Z values for each element

### Animation not working?
Check keyframes exist:
```python
if elem.animation_data and elem.animation_data.action:
    for fcurve in elem.animation_data.action.fcurves:
        print(f"FCurve: {fcurve.data_path}")
```
Expected: 'location' keyframes on Y axis

### Fire not visible?
1. Check material exists: "FastFire" in bpy.data.materials
2. Check emitters exist: Objects named "FireEmitter_*"
3. Switch to Rendered viewport mode
4. Verify Cycles render engine is active

---

## Adding New Tests

When adding functionality, create corresponding tests:

1. **Logic changes**: Update `test_sequential.py`
2. **New functions**: Add unit tests
3. **Visual changes**: Document manual verification steps
4. **Performance changes**: Add timing benchmarks

Example test structure:
```python
def test_new_feature():
    """Test description"""
    # Setup
    input_data = {...}

    # Execute
    result = function_to_test(input_data)

    # Verify
    assert result == expected_value, "Error message"
    print("✓ Test passed")
```

---

## Continuous Integration

For CI/CD pipeline, run:
```bash
# Syntax check
python -m py_compile ALTER_LOGO_SEQUENTIAL.py || exit 1

# Logic tests
python test_sequential.py || exit 1

# If Blender available
blender --background --python ALTER_LOGO_SEQUENTIAL.py || exit 1

echo "All tests passed!"
```

---

## Troubleshooting Test Failures

### test_sequential.py fails
- Check Python version (3.7+)
- Verify logic in animate_sequential()
- Ensure X,Z are not being modified

### Blender execution fails
- Check Blender version (3.0+)
- Verify alter.svg exists
- Check Blender console output for errors
- Ensure bpy module available

### Position overlap detected
- Verify origin_set is called
- Check element.location after import
- Ensure SVG has separate paths for each component

---

## Contributing

When submitting changes:
1. Run all tests (`test_sequential.py`)
2. Verify syntax (`python -m py_compile`)
3. Test in Blender if possible
4. Document any new tests needed
5. Update this TESTING.md with results
