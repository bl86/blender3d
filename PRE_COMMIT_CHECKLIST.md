# PRE-COMMIT CHECKLIST

**MANDATORY CHECKS BEFORE EVERY GIT PUSH**

## ⚠️ CRITICAL: Context Requirements for bpy.ops

**EVERY** `bpy.ops` operator call MUST have proper context. Most operators require:

1. **Selection**: Object must be selected (`obj.select_set(True)`)
2. **Active Object**: Must be set as active (`bpy.context.view_layer.objects.active = obj`)
3. **Deselect Others**: Clear selection first (`bpy.ops.object.select_all(action='DESELECT')`)

### Common Operators and Their Requirements:

| Operator | Requires Selection | Requires Active | Notes |
|----------|-------------------|-----------------|-------|
| `bpy.ops.object.convert()` | ✅ YES | ✅ YES | Must be ONLY object selected |
| `bpy.ops.object.origin_set()` | ✅ YES | ✅ YES | Works on selected objects |
| `bpy.ops.object.duplicate()` | ✅ YES | ✅ YES | Duplicates selected |
| `bpy.ops.object.modifier_add()` | ❌ NO | ✅ YES | Adds to active object |
| `bpy.ops.import_curve.svg()` | ❌ NO | ❌ NO | Import operator |
| `bpy.ops.object.text_add()` | ❌ NO | ❌ NO | Creates new object |

### Standard Pattern:

```python
# ALWAYS use this pattern before operators:
bpy.ops.object.select_all(action='DESELECT')  # Clear selection
obj.select_set(True)                           # Select target
bpy.context.view_layer.objects.active = obj   # Set active

# NOW safe to call operator:
bpy.ops.object.convert(target='MESH')
```

---

## 1. Python Syntax ✅

```bash
python -m py_compile ALTER_LOGO_SEQUENTIAL.py
```

**Expected**: No errors
**If fails**: Fix syntax before proceeding

---

## 2. Logic Tests ✅

```bash
python test_sequential.py
```

**Expected**: `✅ ALL TESTS PASSED`
**If fails**:
- Check animation logic
- Check position preservation
- Check import detection

---

## 3. Search for bpy.ops Calls ✅

```bash
grep -n "bpy.ops\." ALTER_LOGO_SEQUENTIAL.py
```

**For EACH bpy.ops call, verify**:
- [ ] Is selection cleared first? (`bpy.ops.object.select_all(action='DESELECT')`)
- [ ] Is object selected? (`obj.select_set(True)`)
- [ ] Is object active? (`bpy.context.view_layer.objects.active = obj`)

**Common mistakes**:
- ❌ Forgot to deselect all
- ❌ Forgot to select object
- ❌ Forgot to set active object
- ❌ Multiple objects selected when only one should be

---

## 4. Verify All Functions Present ✅

```bash
python -c "
import ast
with open('ALTER_LOGO_SEQUENTIAL.py', 'r') as f:
    tree = ast.parse(f.read())
functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
print('Functions:', ', '.join(functions))
"
```

**Expected functions**:
- clean_scene
- import_svg_preserve_positions
- create_fast_fire_material
- create_fire_for_element
- animate_sequential
- create_banja_luka_text
- create_logo_material
- setup_scene
- main

---

## 5. Check File Dependencies ✅

```bash
ls -lh alter.svg
```

**Expected**: File exists, size > 0
**If fails**: Script will fail at runtime

---

## 6. Review Recent Changes ✅

```bash
git diff ALTER_LOGO_SEQUENTIAL.py
```

**Check**:
- [ ] No debug print statements left in
- [ ] No commented-out code (unless intentional)
- [ ] All changes are intentional
- [ ] Changes match commit message

---

## 7. Run Integration Test (If Blender Available) ✅

```bash
blender --background --python test_blender_integration.py
```

**Expected**: Most tests pass (may need alter.svg)
**If fails**:
- Check error messages
- Verify operator contexts
- Check object states

---

## 8. Test Documentation Match ✅

Check that:
- [ ] TESTING.md reflects actual test commands
- [ ] SEQUENTIAL_README.md describes current behavior
- [ ] All features mentioned in README are implemented
- [ ] No outdated information

---

## 9. Commit Message Quality ✅

Commit message should include:
- [ ] **What** changed (brief summary)
- [ ] **Why** it changed (root cause)
- [ ] **How** it was fixed (solution)
- [ ] **Testing** performed (verification)

Example:
```
Fix: Add proper context for bpy.ops.object.convert()

ROOT CAUSE:
convert() operator requires selected + active object
Was missing deselect_all and select_set calls

SOLUTION:
Added standard context pattern before all convert calls:
1. bpy.ops.object.select_all(action='DESELECT')
2. obj.select_set(True)
3. bpy.context.view_layer.objects.active = obj

TESTING:
✓ Python syntax check
✓ Logic tests pass
✓ Integration test created
✓ All bpy.ops calls verified
```

---

## 10. Final Checks Before Push ✅

- [ ] All tests passing
- [ ] No syntax errors
- [ ] All bpy.ops have proper context
- [ ] Dependencies verified
- [ ] Commit message is detailed
- [ ] Changes are minimal and focused
- [ ] No unrelated changes included

---

## Emergency Rollback

If something breaks after push:

```bash
# Revert last commit
git revert HEAD

# Or reset to previous commit
git reset --hard HEAD~1

# Force push (use carefully)
git push -f origin branch-name
```

---

## Best Practices

1. **Test BEFORE commit** - Don't commit untested code
2. **One issue per commit** - Don't mix multiple fixes
3. **Detailed messages** - Future you will thank you
4. **Small commits** - Easy to review and revert
5. **Run ALL checks** - Don't skip steps

---

## When in Doubt

If unsure about any check:
1. **DON'T PUSH**
2. Test more thoroughly
3. Ask for review
4. Create backup branch

**Remember**: It's better to delay push than to break production!
