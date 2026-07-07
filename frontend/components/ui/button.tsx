// Import the base Button component from the Base UI library
import { Button as ButtonPrimitive } from '@base-ui/react/button'

// Import cva to create different button styles (variants)
// Import VariantProps to provide TypeScript support
import { cva, type VariantProps } from 'class-variance-authority'

// Import the helper function that combines CSS class names
import { cn } from '@/lib/utils'

// Create different styles (variants) for the button
const buttonVariants = cva(

    // Base CSS classes applied to every button
    "group/button inline-flex shrink-0 items-center justify-center rounded-lg border border-transparent bg-clip-padding text-sm font-medium whitespace-nowrap transition-all outline-none select-none focus-visible:border-ring focus-visible:ring-3 focus-visible:ring-ring/50 active:not-aria-[haspopup]:translate-y-px disabled:pointer-events-none disabled:opacity-50 aria-invalid:border-destructive aria-invalid:ring-3 aria-invalid:ring-destructive/20 dark:aria-invalid:border-destructive/50 dark:aria-invalid:ring-destructive/40 [&_svg]:pointer-events-none [&_svg]:shrink-0 [&_svg:not([class*='size-'])]:size-4",

    {

        // Different button styles
        variants: {

            variant: {

                // Blue primary button
                default:
                    'bg-primary text-primary-foreground [a]:hover:bg-primary/80',

                // Button with border
                outline:
                    'border-border bg-background hover:bg-muted hover:text-foreground aria-expanded:bg-muted aria-expanded:text-foreground dark:border-input dark:bg-input/30 dark:hover:bg-input/50',

                // Secondary style button
                secondary:
                    'bg-secondary text-secondary-foreground hover:bg-secondary/80 aria-expanded:bg-secondary aria-expanded:text-secondary-foreground',

                // Transparent button
                ghost:
                    'hover:bg-muted hover:text-foreground aria-expanded:bg-muted aria-expanded:text-foreground dark:hover:bg-muted/50',

                // Red button for delete actions
                destructive:
                    'bg-destructive/10 text-destructive hover:bg-destructive/20 focus-visible:border-destructive/40 focus-visible:ring-destructive/20 dark:bg-destructive/20 dark:hover:bg-destructive/30 dark:focus-visible:ring-destructive/40',

                // Link style button
                link:
                    'text-primary underline-offset-4 hover:underline',
            },

            // Different button sizes
            size: {

                // Normal size
                default:
                    'h-8 gap-1.5 px-2.5 has-data-[icon=inline-end]:pr-2 has-data-[icon=inline-start]:pl-2',

                // Extra small
                xs:
                    "h-6 gap-1 rounded-[min(var(--radius-md),10px)] px-2 text-xs in-data-[slot=button-group]:rounded-lg has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5 [&_svg:not([class*='size-'])]:size-3",

                // Small
                sm:
                    "h-7 gap-1 rounded-[min(var(--radius-md),12px)] px-2.5 text-[0.8rem] in-data-[slot=button-group]:rounded-lg has-data-[icon=inline-end]:pr-1.5 has-data-[icon=inline-start]:pl-1.5 [&_svg:not([class*='size-'])]:size-3.5",

                // Large
                lg:
                    'h-9 gap-1.5 px-2.5 has-data-[icon=inline-end]:pr-2 has-data-[icon=inline-start]:pl-2',

                // Square icon button
                icon:
                    'size-8',

                // Small icon button
                'icon-xs':
                    "size-6 rounded-[min(var(--radius-md),10px)] in-data-[slot=button-group]:rounded-lg [&_svg:not([class*='size-'])]:size-3",

                // Medium icon button
                'icon-sm':
                    'size-7 rounded-[min(var(--radius-md),12px)] in-data-[slot=button-group]:rounded-lg',

                // Large icon button
                'icon-lg':
                    'size-9',
            },
        },

        // Default button style
        defaultVariants: {

            // Use the default blue style
            variant: 'default',

            // Use the default size
            size: 'default',
        },
    },
)

// Create our reusable Button component
function Button({

    // Extra CSS classes
    className,

    // Button style
    variant = 'default',

    // Button size
    size = 'default',

    // Everything else (onClick, disabled, children, etc.)
    ...props

}: ButtonPrimitive.Props &
    VariantProps<typeof buttonVariants>) {

    return (

        // Render the Base UI Button
        <ButtonPrimitive

            // Used internally by the library
            data-slot="button"

            // Combine all CSS classes together
            className={cn(

                buttonVariants({

                    variant,

                    size,

                    className,

                })

            )}

            // Pass remaining props
            {...props}

        />

    );
}

// Export the Button component and its styles
export { Button, buttonVariants }