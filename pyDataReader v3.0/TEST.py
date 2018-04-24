import mgr_binner
import mgr_data

d_mg = mgr_data.DataList()
binner = mgr_binner.Binner(d_mg.data_array, 86400, 60)

binner.create_binned_values()

print(len(binner.binned_data))

for thing in binner.binned_data:
    print(thing.print_values())
